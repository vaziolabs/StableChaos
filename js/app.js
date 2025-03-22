import * as THREE from "https://unpkg.com/three@0.112/build/three.module.js";
import Controller from "./controller.js";
import Engine from "./engine.js";
import Particles from "./particles.js";

export default class App extends Engine {
    constructor(container) {
        super(container);
        
        // Update settings for performance
        THREE.Cache.enabled = true;
        this.renderer.setPixelRatio(window.devicePixelRatio > 1 ? 2 : 1);
        
        // Create particle system
        this.particleSystem = new Particles(this.scene);
        this.particleSystem.setParticleCount(10000);
        
        this.controller = new Controller(this);
        this.particleSystem.setController(this.controller);
        this.setParticleSystem(this.particleSystem);
        
        this.particleSystem.init();
        
        // Add performance monitor
        this.setupPerformanceMonitor();
    }
    
    setupPerformanceMonitor() {
        // Simple FPS counter
        const fpsDisplay = document.createElement('div');
        fpsDisplay.style.position = 'absolute';
        fpsDisplay.style.top = '10px';
        fpsDisplay.style.right = '10px';
        fpsDisplay.style.color = 'white';
        fpsDisplay.style.fontFamily = 'monospace';
        fpsDisplay.style.padding = '5px';
        fpsDisplay.style.backgroundColor = 'rgba(0,0,0,0.5)';
        document.body.appendChild(fpsDisplay);
        
        let lastTime = performance.now();
        let frames = 0;
        
        this.addPreRenderCallback(() => {
            frames++;
            const now = performance.now();
            if (now - lastTime > 1000) {
                const fps = Math.round(frames * 1000 / (now - lastTime));
                fpsDisplay.textContent = `FPS: ${fps} | Particles: ${this.particleSystem.positions.length/3}`;
                frames = 0;
                lastTime = now;
            }
        });
    }
    
    init() {
        this.start();
    }
}
