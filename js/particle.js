import * as THREE from "https://unpkg.com/three@0.112/build/three.module.js";

export default class Particle {
    constructor(scene, index) {
        this.scene = scene;
        this.mesh = null;
        this.position = new THREE.Vector3();
        this.velocity = new THREE.Vector3();
        this.energy = 1.0;
        this.particleType = 'a';
        this.isDead = false;
        this.createMesh();
    }

    createMesh() {
        const geometry = new THREE.SphereGeometry(0.2, 16, 16);
        const material = new THREE.MeshPhongMaterial({
            color: new THREE.Color(1, 1, 1),
            emissive: new THREE.Color(1, 1, 1),
            emissiveIntensity: 0.5,
            transparent: true,
            opacity: 0.8
        });
        this.mesh = new THREE.Mesh(geometry, material);
        
        this.mesh.position.set(0, 0, 0);
        this.velocity = new THREE.Vector3(
            (Math.random() - 0.5) * 0.02,
            (Math.random() - 0.5) * 0.02,
            (Math.random() - 0.5) * 0.02
        );
        
        this.scene.add(this.mesh);
    }

    update(particles) {
        if (this.mesh && this.mesh.scale) {
            const scale = 0.5 + this.energy * 0.5;
            this.mesh.scale.set(scale, scale, scale);
        }

        // Removed random velocity additions
        if (this.velocity.length() > 0.2) {
            this.velocity.normalize().multiplyScalar(0.2);
        }
        
        this.mesh.position.add(this.velocity);
        
        const boundaryLimit = 10;
        if (Math.abs(this.mesh.position.x) > boundaryLimit) {
            this.velocity.x *= -1;
            this.mesh.position.x = Math.sign(this.mesh.position.x) * boundaryLimit;
        }
        if (Math.abs(this.mesh.position.y) > boundaryLimit) {
            this.velocity.y *= -1;
            this.mesh.position.y = Math.sign(this.mesh.position.y) * boundaryLimit;
        }
        if (Math.abs(this.mesh.position.z) > boundaryLimit) {
            this.velocity.z *= -1;
            this.mesh.position.z = Math.sign(this.mesh.position.z) * boundaryLimit;
        }
        
        this.applyForces(particles);
    }

    applyForces(particles) {
        // Use pre-calculated relationship map for faster access
        const { typeMap, globalAttraction, particleTypes } = this.scene.userData.particles || {};
        
        for (const other of particles) {
            if (other === this) continue;

            const distance = this.mesh.position.distanceTo(other.mesh.position);
            
            // Skip particles that are too far away
            if (distance > 15) continue;
            
            const direction = new THREE.Vector3()
                .subVectors(other.mesh.position, this.mesh.position)
                .normalize();
            
            // Get strength based on global attraction and this particle's bias only
            let strength = 0;
            if (typeMap) {
                // Basic strength from global attraction
                strength = globalAttraction;
                
                // Add this particle's bias for the relationship type
                if (this.particleType === other.particleType) {
                    // For same type, add the same-type bias
                    strength += particleTypes[this.particleType].sameTypeBias || 0;
                } else {
                    // For different types, use the appropriate relationship bias
                    const relationType = this.scene.userData.controller?.topical?.getRelationshipType(this.particleType, other.particleType);
                    strength += particleTypes[this.particleType][`${relationType}Bias`] || 0;
                }
            } else {
                // Fallback to controller method
                const controller = this.scene.userData.controller;
                if (controller?.topical) {
                    if (this.particleType === other.particleType) {
                        strength = controller.topical.getGlobalAttraction() + 
                                   controller.topical.getParticleSameTypeBias(this.particleType);
                    } else {
                        strength = controller.topical.getGlobalAttraction() + 
                                   controller.topical.getParticleBias(this.particleType, other.particleType);
                    }
                }
            }
            
            const distanceFactor = 1 / (1 + distance * distance);
            const scaledStrength = strength * distanceFactor * 0.1;
            
            this.velocity.add(direction.multiplyScalar(scaledStrength));
        }
        this.velocity.multiplyScalar(0.98); // Slightly stronger damping
    }
    
    setColor(color) {
        if (this.mesh && this.mesh.material) {
            this.mesh.material.color.copy(color);
            this.mesh.material.emissive.copy(color);
        }
    }

    setType(type) {
        this.particleType = type;
    }

    parseTypeToBits(type) {
        const controller = this.scene.userData.controller;
        if (controller && controller.topical) {
            return controller.topical.getTypeBits(type);
        }
        
        // Fallback implementation
        const bitMap = {
            a: [0, 0, 0], b: [1, 0, 0], c: [0, 1, 0], d: [1, 1, 0],
            e: [0, 0, 1], f: [1, 0, 1], g: [0, 1, 1], h: [1, 1, 1]
        };
        return bitMap[type] || [0, 0, 0];
    }

    getRelationshipStrength(aType, bType, diffCount) {
        const controller = this.scene.userData.controller;
        if (controller && controller.topical) {
            return controller.topical.getAttractionValue(aType, bType);
        }
        return 0;
    }
}