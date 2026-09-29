import './style.css';

import { simplex2d } from 'math/noise';
import { mulberry32 } from 'math/random';

type SubsystemName = 'motor' | 'procedural' | 'executive' | 'memory';

const subsystemNames: SubsystemName[] = ['motor', 'procedural', 'executive', 'memory'];
const colors = ['#ff6680', '#ffc857', '#6fe7dd', '#9e8cff'];
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
canvas.setAttribute('role', 'img');
canvas.setAttribute(
  'aria-label',
  'Conceptual state field showing four subsystem trajectories converging toward one coarse observable.',
);
mount.appendChild(canvas);

const maybeContext = canvas.getContext('2d', { alpha: true });
if (!maybeContext) throw new Error('Canvas2D context unavailable');
const context: CanvasRenderingContext2D = maybeContext;

let width = 0;
let height = 0;
let dpr = 1;

function resize(): void {
  dpr = Math.min(window.devicePixelRatio || 1, 2);
  width = window.innerWidth;
  height = window.innerHeight;
  canvas.width = Math.floor(width * dpr);
  canvas.height = Math.floor(height * dpr);
  canvas.style.width = width + 'px';
  canvas.style.height = height + 'px';
  context.setTransform(dpr, 0, 0, dpr, 0, 0);
}

window.addEventListener('resize', resize);
resize();

interface Particle {
  group: number;
  progress: number;
  phase: number;
  speedBias: number;
  radiusBias: number;
}

const noise = simplex2d.create(73);
const rng = mulberry32.create(42);
const particles: Particle[] = [];
const particlesPerGroup = 24;

for (let group = 0; group < 4; group += 1) {
  for (let index = 0; index < particlesPerGroup; index += 1) {
    particles.push({
      group,
      progress: mulberry32.sample(rng),
      phase: mulberry32.sample(rng) * 100,
      speedBias: 0.72 + mulberry32.sample(rng) * 0.62,
      radiusBias: 0.72 + mulberry32.sample(rng) * 0.85,
    });
  }
}

function layout() {
  const panelWidth = Math.min(470, Math.max(320, width - 32));
  const startX = width < 820 ? 40 : Math.max(panelWidth + 90, width * 0.34);
  const portalX = width < 820 ? width * 0.72 : width * 0.80;
  const portalY = height * 0.5;
  const spread = Math.min(height * 0.56, 430);
  const top = portalY - spread / 2;
  const laneY = subsystemNames.map((_, index) => top + (spread * index) / 3);
  return { startX, portalX, portalY, laneY };
}

function drawGlow(x: number, y: number, radius: number, color: string, alpha = 1): void {
  context.save();
  context.globalAlpha = alpha;
  const glow = context.createRadialGradient(x, y, 0, x, y, radius * 3.4);
  glow.addColorStop(0, color);
  glow.addColorStop(0.22, color + 'cc');
  glow.addColorStop(0.48, color + '44');
  glow.addColorStop(1, color + '00');
  context.fillStyle = glow;
  context.beginPath();
  context.arc(x, y, radius * 3.4, 0, Math.PI * 2);
  context.fill();
  context.restore();
}

function drawPortal(x: number, y: number, active: boolean): void {
  const color = active ? '#d7ff5d' : '#ff8d8d';
  drawGlow(x, y, 18, color, 0.9);

  context.save();
  context.strokeStyle = color;
  context.lineWidth = 1.5;
  context.globalAlpha = 0.85;
  context.beginPath();
  context.arc(x, y, 18, 0, Math.PI * 2);
  context.stroke();

  context.globalAlpha = 0.28;
  context.beginPath();
  context.arc(x, y, 34, 0, Math.PI * 2);
  context.stroke();

  context.font = '600 11px ui-monospace, SFMono-Regular, Menlo, monospace';
  context.textAlign = 'center';
  context.fillStyle = color;
  context.globalAlpha = 0.95;
  context.fillText('OBSERVABLE', x, y + 55);
  context.restore();
}

function drawLane(
  group: number,
  sourceX: number,
  sourceY: number,
  portalX: number,
  portalY: number,
): void {
  const name = subsystemNames[group];
  const accessibility = state[name];
  const color = colors[group];
  const reach = 0.50 + accessibility * 0.50;
  const endX = sourceX + (portalX - sourceX) * reach;
  const endY = sourceY + (portalY - sourceY) * accessibility;

  context.save();
  context.strokeStyle = color;
  context.globalAlpha = 0.11 + accessibility * 0.14;
  context.lineWidth = 1.1;
  context.setLineDash([3, 10]);
  context.beginPath();
  context.moveTo(sourceX, sourceY);
  context.bezierCurveTo(
    sourceX + (portalX - sourceX) * 0.35,
    sourceY,
    sourceX + (portalX - sourceX) * 0.68,
    endY,
    endX,
    endY,
  );
  context.stroke();
  context.setLineDash([]);

  drawGlow(sourceX, sourceY, 9, color, 0.72);
  context.fillStyle = color;
  context.globalAlpha = 0.95;
  context.beginPath();
  context.arc(sourceX, sourceY, 5.5, 0, Math.PI * 2);
  context.fill();

  context.font = '600 10px ui-monospace, SFMono-Regular, Menlo, monospace';
  context.textAlign = 'right';
  context.fillStyle = '#f3efe6';
  context.globalAlpha = 0.72;
  context.fillText(name.toUpperCase(), sourceX - 16, sourceY + 4);
  context.restore();
}

function advanceAndDrawParticle(
  particle: Particle,
  elapsed: number,
  dt: number,
  sourceX: number,
  sourceY: number,
  portalX: number,
  portalY: number,
): void {
  const name = subsystemNames[particle.group];
  const accessibility = state[name];
  const color = colors[particle.group];

  if (!reducedMotion) {
    const speed = (0.052 + accessibility * 0.12) * particle.speedBias;
    particle.progress += dt * speed;
    if (particle.progress > 1) {
      particle.progress -= 1;
      particle.phase = mulberry32.sample(rng) * 100;
    }
  }

  const p = particle.progress;
  const eased = p * p * (3 - 2 * p);
  const reach = 0.50 + 0.50 * accessibility;
  const localP = eased * reach;

  const x = sourceX + (portalX - sourceX) * localP;
  const convergence = Math.pow(eased, 1.65) * accessibility;
  const baseY = sourceY + (portalY - sourceY) * convergence;

  const n1 = simplex2d.sample(
    noise,
    particle.phase + p * 1.65,
    elapsed * 0.06 + particle.group * 0.8,
  );
  const n2 = simplex2d.sample(
    noise,
    particle.phase + 17.2,
    elapsed * 0.045 + p * 1.35,
  );

  const amplitude = 7 + (1 - accessibility) * 20;
  const y = baseY + n1 * amplitude;
  const radius = (2.1 + accessibility * 1.7 + n2 * 0.45) * particle.radiusBias;

  context.save();
  context.globalCompositeOperation = 'lighter';
  context.shadowBlur = 12 + accessibility * 10;
  context.shadowColor = color;
  context.globalAlpha = 0.40 + accessibility * 0.48;
  context.fillStyle = color;
  context.beginPath();
  context.arc(x, y, Math.max(1.4, radius), 0, Math.PI * 2);
  context.fill();
  context.restore();
}

let previous = performance.now() / 1000;

function render(nowMs: number): void {
  const elapsed = nowMs / 1000;
  const dt = Math.min(Math.max(elapsed - previous, 0), 0.05);
  previous = elapsed;

  context.clearRect(0, 0, width, height);

  const { startX, portalX, portalY, laneY } = layout();
  const complexAction = state.motor >= 0.5 && state.procedural >= 0.5;

  context.save();
  context.globalAlpha = 0.14;
  context.strokeStyle = '#d7ff5d';
  context.lineWidth = 1;
  for (let r = 90; r <= Math.min(width, height) * 0.58; r += 88) {
    context.beginPath();
    context.arc(portalX, portalY, r, 0, Math.PI * 2);
    context.stroke();
  }
  context.restore();

  for (let group = 0; group < 4; group += 1) {
    drawLane(group, startX, laneY[group], portalX, portalY);
  }

  for (const particle of particles) {
    advanceAndDrawParticle(
      particle,
      elapsed,
      dt,
      startX,
      laneY[particle.group],
      portalX,
      portalY,
    );
  }

  drawPortal(portalX, portalY, complexAction);

  requestAnimationFrame(render);
}

requestAnimationFrame(render);
