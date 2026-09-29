import './style.css';

import {
  attribute,
  cameraProjectionMatrix,
  cameraViewMatrix,
  createCanvasTarget,
  createMaterial,
  createSphereGeometry,
  d,
  f32,
  frame,
  fullscreen,
  init,
  Mesh,
  modelNormalMatrix,
  modelWorldMatrix,
  mul,
  normalize,
  PerspectiveCamera,
  renderOutput,
  renderTexture,
  Scene,
  varying,
  vec3,
  vec4,
  webgl,
} from 'gpucat';
import { simplex2d } from 'math/noise';
import { mulberry32 } from 'math/random';

type SubsystemName = 'motor' | 'procedural' | 'executive' | 'memory';

const subsystemNames: SubsystemName[] = ['motor', 'procedural', 'executive', 'memory'];
const laneY = [1.5, 0.5, -0.5, -1.5];
const colors = [
  [1.0, 0.30, 0.43],
  [1.0, 0.64, 0.18],
  [0.25, 0.83, 0.78],
  [0.54, 0.45, 1.0],
] as const;

const state: Record<SubsystemName, number> = {
  motor: 1,
  procedural: 1,
  executive: 1,
  memory: 1,
};

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

function dissociationIndex(values: number[]): number {
  let numerator = 0;
  for (let i = 0; i < values.length; i += 1) {
    for (let j = i + 1; j < values.length; j += 1) {
      numerator += Math.abs(values[i] - values[j]);
    }
  }
  return numerator / Math.floor((values.length * values.length) / 4);
}

function readState(): number[] {
  return subsystemNames.map((name) => state[name]);
}

function updateHud(): void {
  const values = readState();
  const complexAction = state.motor >= 0.5 && state.procedural >= 0.5;
  document.querySelector<HTMLElement>('#state-vector')!.textContent =
    '[' + values.map((value) => value.toFixed(2)).join(', ') + ']';
  document.querySelector<HTMLElement>('#d-index')!.textContent =
    dissociationIndex(values).toFixed(3);
  const observable = document.querySelector<HTMLElement>('#observable')!;
  observable.textContent = 'complex_action = ' + String(complexAction);
  observable.dataset.true = String(complexAction);
}

for (const name of subsystemNames) {
  const input = document.querySelector<HTMLInputElement>('#' + name)!;
  const output = document.querySelector<HTMLOutputElement>('#' + name + '-out')!;
  input.addEventListener('input', () => {
    state[name] = Number(input.value);
    output.value = state[name].toFixed(2);
    updateHud();
  });
}

function setPreset(values: number[]): void {
  subsystemNames.forEach((name, index) => {
    state[name] = values[index];
    const input = document.querySelector<HTMLInputElement>('#' + name)!;
    const output = document.querySelector<HTMLOutputElement>('#' + name + '-out')!;
    input.value = String(values[index]);
    output.value = values[index].toFixed(2);
  });
  updateHud();
}

document.querySelector<HTMLButtonElement>('#integrated')!.addEventListener('click', () => {
  setPreset([1, 1, 1, 1]);
});

document.querySelector<HTMLButtonElement>('#dissociated')!.addEventListener('click', () => {
  setPreset([1, 1, 0, 0]);
});

const uiRng = mulberry32.create(20260929);
document.querySelector<HTMLButtonElement>('#randomize')!.addEventListener('click', () => {
  setPreset(subsystemNames.map(() => mulberry32.sample(uiRng)));
});

updateHud();

const mount = document.querySelector<HTMLElement>('#scene')!;
const canvas = document.createElement('canvas');
mount.appendChild(canvas);

const view = createCanvasTarget(canvas, { samples: 4 });
view.setPixelRatio(Math.min(devicePixelRatio, 2));
view.setSize(window.innerWidth, window.innerHeight);

const renderer = await init(webgl({ target: view }));
const scene = new Scene();

const camera = new PerspectiveCamera(Math.PI / 4, window.innerWidth / window.innerHeight, 0.1, 100);
camera.position[2] = 8.2;
scene.add(camera);

window.addEventListener('resize', () => {
  view.setSize(window.innerWidth, window.innerHeight);
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
});

const position = attribute('position', d.vec3f);
const normal = attribute('normal', d.vec3f);
const worldPosition = mul(modelWorldMatrix, vec4(position, f32(1)));
const clipPosition = mul(cameraProjectionMatrix, mul(cameraViewMatrix, worldPosition));
const vWorldNormal = varying(normalize(mul(modelNormalMatrix, normal)), 'vNormal');
const lightDirection = vec3(0.35, 0.9, 0.7).normalize();
const lighting = f32(0.28).add(vWorldNormal.dot(lightDirection).max(f32(0)));

function material(rgb: readonly [number, number, number]) {
  return createMaterial({
    vertex: clipPosition,
    fragment: vec4(vec3(rgb[0], rgb[1], rgb[2]).mul(lighting), f32(1)),
  });
}

const particleGeometry = createSphereGeometry(0.055, 10, 7);
const coreGeometry = createSphereGeometry(0.12, 16, 10);
const portalGeometry = createSphereGeometry(0.22, 20, 12);
const materials = colors.map((color) => material(color));

const portal = new Mesh(portalGeometry, material([0.75, 0.95, 0.28]));
portal.position[0] = 2.45;
portal.position[1] = 0;
portal.position[2] = 0;
scene.add(portal);

for (let group = 0; group < 4; group += 1) {
  const core = new Mesh(coreGeometry, materials[group]);
  core.position[0] = -3.35;
  core.position[1] = laneY[group];
  core.position[2] = 0;
  scene.add(core);
}

interface Particle {
  mesh: Mesh;
  group: number;
  progress: number;
  phase: number;
  speedBias: number;
}

const noise = simplex2d.create(73);
const rng = mulberry32.create(42);
const particles: Particle[] = [];
const particlesPerGroup = 18;

for (let group = 0; group < 4; group += 1) {
  for (let index = 0; index < particlesPerGroup; index += 1) {
    const mesh = new Mesh(particleGeometry, materials[group]);
    scene.add(mesh);
    particles.push({
      mesh,
      group,
      progress: mulberry32.sample(rng),
      phase: mulberry32.sample(rng) * 100,
      speedBias: 0.75 + mulberry32.sample(rng) * 0.5,
    });
  }
}

function updateParticle(particle: Particle, elapsed: number, dt: number): void {
  const name = subsystemNames[particle.group];
  const accessibility = state[name];
  const speed = (0.055 + accessibility * 0.12) * particle.speedBias;
  particle.progress += dt * speed * (reducedMotion ? 0.18 : 1);

  if (particle.progress > 1) {
    particle.progress -= 1;
    particle.phase = mulberry32.sample(rng) * 100;
  }

  const p = particle.progress;
  const reach = 0.66 + 0.34 * accessibility;
  const x = -3.2 + 5.65 * p * reach;
  const convergence = Math.pow(p, 1.7) * accessibility;
  const n1 = simplex2d.sample(noise, particle.phase + p * 1.4, elapsed * 0.035 + particle.group);
  const n2 = simplex2d.sample(noise, particle.phase + 19, elapsed * 0.028 + p * 1.2);
  const baseY = laneY[particle.group];
  const y = baseY * (1 - convergence) + n1 * (0.10 + (1 - accessibility) * 0.20);
  const z = n2 * 0.28;

  particle.mesh.position[0] = x;
  particle.mesh.position[1] = y;
  particle.mesh.position[2] = z;
  particle.mesh.updateWorldMatrix();
}

const scenePass = renderTexture(scene, camera);
const composite = fullscreen(renderOutput(scenePass.getTextureNode()));

let previous = performance.now() / 1000;

function render(nowMs: number): void {
  const elapsed = nowMs / 1000;
  const dt = Math.min(elapsed - previous, 0.05);
  previous = elapsed;

  for (const particle of particles) updateParticle(particle, elapsed, dt);

  scene.updateWorldMatrix();
  camera.updateViewMatrix();

  const f = frame(renderer);
  const pass = f.pass({ target: view });
  pass.draw(composite);
  pass.end();
  f.submit();

  requestAnimationFrame(render);
}

requestAnimationFrame(render);
