import { GUI } from "https://unpkg.com/three@0.112/examples/jsm/libs/dat.gui.module.js";
import Topical from "./topical.js";

export default class Controller {
    constructor(engine) {
        this.engine = engine;
        this.gui = new GUI();
        
        this.params = {
            particlesPerType: 1000,
            baseAttractions: {
                sameType: 0.0,
                orthogonal: 0.0,
                diagonal: 0.0,
                polar: 0.0
            },
            particleTypes: {
                a: { color: "#00FF00", sameTypeBias: -1.0, orthogonalBias: 0.75, diagonalBias: 0.35, polarBias: -0.1 },
                b: { color: "#FF0000", sameTypeBias: -1.0, orthogonalBias: 0.75, diagonalBias: 0.35, polarBias: -0.1 },
                c: { color: "#0000FF", sameTypeBias: -1.0, orthogonalBias: 0.75, diagonalBias: 0.35, polarBias: -0.1 },
                d: { color: "#FFFF00", sameTypeBias: -1.0, orthogonalBias: 0.75, diagonalBias: 0.35, polarBias: -0.1 },
                e: { color: "#FF00FF", sameTypeBias: -1.0, orthogonalBias: 0.75, diagonalBias: 0.35, polarBias: -0.1 },
                f: { color: "#00FFFF", sameTypeBias: -1.0, orthogonalBias: 0.75, diagonalBias: 0.35, polarBias: -0.1 },
                g: { color: "#FFFFFF", sameTypeBias: -1.0, orthogonalBias: 0.75, diagonalBias: 0.35, polarBias: -0.1 },
                h: { color: "#FF8800", sameTypeBias: -1.0, orthogonalBias: 0.75, diagonalBias: 0.35, polarBias: -0.1 }
            }
        };
        
        this.topical = new Topical(this.params);
        this.relationshipGrid = [];
        this.selectedType = 'a';
        this.biasPanel = null; // Initialize it here
        this.setupGUI();
    }
    
    setupGUI() {
        const particleSystemFolder = this.gui.addFolder('Core Settings');
        particleSystemFolder.add(this.params, 'particlesPerType', 0, 2500).step(1)
            .onChange(() => {
                this.engine.particleSystem.init();
                this.topical.updateFromParams(this.params);
            });
        
        const addBaseSlider = (prop, name) => {
            particleSystemFolder.add(this.params.baseAttractions, prop, -1, 1)
                .name(name)
                .onChange(() => {
                    this.topical.updateFromParams(this.params);
                    this.engine.particleSystem.updateFromController();
                });
        };
        
        addBaseSlider('sameType', 'Same Type');
        addBaseSlider('orthogonal', 'Adjacent');
        addBaseSlider('diagonal', 'Diagonal');
        addBaseSlider('polar', 'Polar');
        
        this.setup3DCubeVisualization();
        this.setupBiasControls();
    }
    
    setup3DCubeVisualization() {
        const cubeContainer = document.createElement('div');
        cubeContainer.style.position = 'relative';
        cubeContainer.style.width = '280px';
        cubeContainer.style.height = '280px';
        cubeContainer.style.margin = '10px auto';
        cubeContainer.style.perspective = '800px';
        
        this.cube = document.createElement('div');
        this.cube.style.position = 'absolute';
        this.cube.style.width = '100%';
        this.cube.style.height = '100%';
        this.cube.style.transformStyle = 'preserve-3d';
        this.cube.style.transform = 'rotateX(20deg) rotateY(30deg)';
        
        // Set up mouse rotation
        let isDragging = false;
        let lastMouseX = 0;
        let lastMouseY = 0;
        let rotateX = 20;
        let rotateY = 30;
        
        cubeContainer.addEventListener('mousedown', (e) => {
            isDragging = true;
            lastMouseX = e.clientX;
            lastMouseY = e.clientY;
            e.preventDefault();
        });
        
        document.addEventListener('mousemove', (e) => {
            if (isDragging) {
                const deltaX = e.clientX - lastMouseX;
                const deltaY = e.clientY - lastMouseY;
                
                rotateY += deltaX * 0.5;
                rotateX -= deltaY * 0.5;
                
                rotateX = Math.max(-60, Math.min(60, rotateX));
                
                this.cube.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
                
                // Update all node billboards to face the camera
                document.querySelectorAll('.node-content').forEach(content => {
                    content.style.transform = `rotateY(${-rotateY}deg) rotateX(${-rotateX}deg)`;
                });
                
                lastMouseX = e.clientX;
                lastMouseY = e.clientY;
            }
        });
        
        document.addEventListener('mouseup', () => {
            isDragging = false;
        });
        
        // Create nodes with proper 3D coordinates aligned with bit positions
        const nodePositions = {
            a: {x: -1, y: -1, z: -1},  // 000
            b: {x: 1, y: -1, z: -1},  // 100
            c: {x: -1, y: 1, z: -1},  // 010
            d: {x: 1, y: 1, z: -1},  // 110
            e: {x: -1, y: -1, z: 1},  // 001
            f: {x: 1, y: -1, z: 1},  // 101
            g: {x: -1, y: 1, z: 1},  // 011
            h: {x: 1, y: 1, z: 1}   // 111
        };
        
        // Generate connections based on fixed relationship definitions
        const connections = [];
        
        // Define relationships according to user specification
        const relationshipMap = {
            orthogonal: ['ab', 'ac', 'bd', 'cd', 'ae', 'bf', 'cg', 'dh', 'ef', 'eg', 'gh', 'fh'],
            diagonal: ['ad', 'af', 'ag', 'bc', 'be', 'bh', 'ce', 'ch', 'df', 'dg', 'eh', 'fg'],
            polar: ['ah', 'bg', 'cf', 'de']
        };

        Object.entries(relationshipMap).forEach(([relType, pairs]) => {
            pairs.forEach(pair => {
                const from = pair[0].toLowerCase();
                const to = pair[1].toLowerCase();
                
                connections.push({
                    from,
                    to,
                    type: relType,
                    posA: nodePositions[from],
                    posB: nodePositions[to]
                });
            });
        });
        
        // Store node elements for later reference
        this.nodeElements = {};
        
        // Create connection container
        const connectionsContainer = document.createElement('div');
        connectionsContainer.className = 'connections-container';
        connectionsContainer.style.position = 'absolute';
        connectionsContainer.style.width = '100%';
        connectionsContainer.style.height = '100%';
        connectionsContainer.style.transformStyle = 'preserve-3d';
        this.cube.appendChild(connectionsContainer);
        
        // Create all nodes first
        Object.entries(nodePositions).forEach(([type, pos]) => {
            const node = this.createCubeNode(type, pos);
            this.nodeElements[type] = node;
            this.cube.appendChild(node);
        });
        
        // Create all connections
        connections.forEach(conn => {
            const connection = document.createElement('div');
            connection.className = 'connection';
            connection.dataset.connection = `${conn.from}-${conn.to}`;
            connection.dataset.relationshipType = conn.type;
            connection.style.position = 'absolute';
            connection.style.transformStyle = 'preserve-3d';
            
            const posA = conn.posA;
            const posB = conn.posB;
            const scale = 60;
            const center = 140;
            
            // Calculate midpoint for the connection
            const midX = (posA.x + posB.x) / 2 * scale + center;
            const midY = (posA.y + posB.y) / 2 * scale + center;
            const midZ = (posA.z + posB.z) / 2 * scale;
            
            connection.style.left = `${midX}px`;
            connection.style.top = `${midY}px`;
            
            // Calculate distance and rotation
            const dx = posB.x - posA.x;
            const dy = posB.y - posA.y;
            const dz = posB.z - posA.z;
            
            const length = Math.sqrt(dx*dx + dy*dy + dz*dz) * scale;
            
            // Create cylinder instead of line
            const cylinder = document.createElement('div');
            cylinder.className = 'connection-cylinder';
            cylinder.style.position = 'absolute';
            cylinder.style.width = `${length}px`;
            cylinder.style.height = '6px';
            cylinder.style.borderRadius = '3px';
            cylinder.style.backgroundColor = '#FFFFFF';
            cylinder.style.transformOrigin = 'left center';
            cylinder.style.left = '0';
            cylinder.style.top = '-3px';
            
            // Calculate rotations
            const yaw = Math.atan2(dy, dx) * 180 / Math.PI;
            const pitch = Math.atan2(dz, Math.sqrt(dx*dx + dy*dy)) * 180 / Math.PI;
            
            // Create multiple cylinder segments to give a 3D appearance from all angles
            for (let i = 0; i < 4; i++) {
                const segment = cylinder.cloneNode();
                segment.style.transform = `rotateZ(${yaw}deg) rotateY(${pitch}deg) rotateX(${i * 45}deg) translateX(-50%)`;
                connection.appendChild(segment);
            }
            
            connection.style.transform = `translateZ(${midZ}px)`;
            connectionsContainer.appendChild(connection);
        });
        
        cubeContainer.appendChild(this.cube);
        this.gui.__ul.appendChild(cubeContainer);
        
        this.updateCubeConnections();
        this.highlightSelectedNode();
        this.updateSelectedTypeIndicator();
    }

    createCubeNode(type, pos) {
        const scale = 60;
        const center = 140;
        const size = 20;
        const halfSize = size / 2;
        
        // Create outer node container that handles 3D positioning
        const node = document.createElement('div');
        node.style.position = 'absolute';
        node.style.width = `${size}px`;
        node.style.height = `${size}px`;
        node.style.transformStyle = 'preserve-3d';
        node.style.transform = `translate3d(${pos.x * scale + center - halfSize}px, ${pos.y * scale + center - halfSize}px, ${pos.z * scale}px)`;
        node.dataset.type = type;
        node.style.zIndex = '100'; // Put nodes in front
        
        // Create inner content that will rotate to face camera
        const nodeContent = document.createElement('div');
        nodeContent.className = 'node-content';
        nodeContent.style.position = 'absolute';
        nodeContent.style.width = '100%';
        nodeContent.style.height = '100%';
        nodeContent.style.borderRadius = '50%';
        nodeContent.style.backgroundColor = this.params.particleTypes[type].color;
        nodeContent.style.cursor = 'pointer';
        nodeContent.style.boxSizing = 'border-box';
        nodeContent.style.boxShadow = '0 0 10px rgba(0,0,0,0.3)';
        nodeContent.style.transform = 'rotateY(0deg) rotateX(0deg)'; // Initial billboard orientation
        nodeContent.style.transformStyle = 'preserve-3d';
        
        // Add a label inside the node
        const label = document.createElement('span');
        label.textContent = type.toUpperCase();
        label.style.position = 'absolute';
        label.style.top = '50%';
        label.style.left = '50%';
        label.style.transform = 'translate(-50%, -50%)';
        label.style.fontSize = '10px';
        label.style.fontWeight = 'bold';
        label.style.color = this.getContrastColor(this.params.particleTypes[type].color);
        
        nodeContent.appendChild(label);
        node.appendChild(nodeContent);
        
        node.addEventListener('click', () => {
            this.selectedType = type;
            this.updateBiasControls();
            this.updateCubeConnections();
            this.highlightSelectedNode();
        });
        
        // Remove the outline/border if there was one
        nodeContent.style.border = 'none';
        
        return node;
    }

    updateCubeConnections() {
        document.querySelectorAll('.connection-cylinder').forEach(cylinder => {
            const connection = cylinder.parentElement;
            if (!connection.dataset.connection) return;
            
            const [typeA, typeB] = connection.dataset.connection.split('-');
            
            // Get fresh attraction value from our corrected topical mapping
            const attraction = this.topical.getAttractionValue(typeA, typeB);
            
            // Blue for attraction, red for repulsion
            const hue = attraction > 0 ? 240 : 0;
            const thickness = Math.abs(attraction) * 5 + 3;
            
            cylinder.style.backgroundColor = `hsl(${hue}, 80%, 50%)`;
            cylinder.style.height = `${thickness}px`;
            cylinder.style.opacity = Math.abs(attraction) * 0.8 + 0.2;
            
            // Highlight connections to selected node
            if (typeA === this.selectedType || typeB === this.selectedType) {
                cylinder.style.boxShadow = `0 0 5px hsl(${hue}, 80%, 50%)`;
                cylinder.style.zIndex = '10';
            } else {
                cylinder.style.boxShadow = 'none';
                cylinder.style.zIndex = '1';
            }
        });
    }

    updateBiasControls() {
        if (this.biasPanel) {
            this.biasPanel.remove();
        }
        
        this.setupBiasControls();
    }

    setupBiasControls() {
        if (this.biasPanel) {
            this.biasPanel.remove();
        }
        
        this.biasPanel = document.createElement('div');
        this.biasPanel.className = 'bias-panel';
        this.biasPanel.style.padding = '10px';
        this.biasPanel.style.borderTop = '1px solid #ccc';
        
        const title = document.createElement('div');
        title.style.fontWeight = 'bold';
        title.style.marginBottom = '5px';
        this.updateSelectedTypeIndicator();
        
        this.biasPanel.appendChild(title);
        
        // Add control for same-type bias
        const sameTypeControl = document.createElement('div');
        sameTypeControl.style.marginBottom = '5px';
        
        // Create a visualizer showing same type 
        const visualizer = document.createElement('div');
        visualizer.style.display = 'flex';
        visualizer.style.gap = '5px';
        visualizer.style.marginBottom = '5px';
        
        const sameTypeNode = document.createElement('span');
        sameTypeNode.textContent = this.selectedType.toUpperCase();
        sameTypeNode.style.width = '20px';
        sameTypeNode.style.height = '20px';
        sameTypeNode.style.borderRadius = '50%';
        sameTypeNode.style.backgroundColor = this.params.particleTypes[this.selectedType].color;
        sameTypeNode.style.color = this.getContrastColor(this.params.particleTypes[this.selectedType].color);
        sameTypeNode.style.display = 'flex';
        sameTypeNode.style.alignItems = 'center';
        sameTypeNode.style.justifyContent = 'center';
        sameTypeNode.style.fontSize = '10px';
        visualizer.appendChild(sameTypeNode);
        
        const sameTypeLabel = document.createElement('label');
        sameTypeLabel.textContent = 'Same Type Bias: ';
        sameTypeLabel.style.display = 'inline-block';
        sameTypeLabel.style.width = '100px';
        
        const sameTypeSlider = document.createElement('input');
        sameTypeSlider.type = 'range';
        sameTypeSlider.min = -1;
        sameTypeSlider.max = 1;
        sameTypeSlider.step = 0.01;
        sameTypeSlider.value = this.params.particleTypes[this.selectedType].sameTypeBias || 0;
        sameTypeSlider.style.width = '150px';
        sameTypeSlider.style.verticalAlign = 'middle';
        
        const sameTypeValueDisplay = document.createElement('span');
        sameTypeValueDisplay.textContent = sameTypeSlider.value;
        sameTypeValueDisplay.style.display = 'inline-block';
        sameTypeValueDisplay.style.width = '40px';
        sameTypeValueDisplay.style.textAlign = 'right';
        
        sameTypeSlider.addEventListener('input', (e) => {
            this.params.particleTypes[this.selectedType].sameTypeBias = parseFloat(e.target.value);
            sameTypeValueDisplay.textContent = parseFloat(e.target.value).toFixed(2);
            
            // Force update all parameters
            this.topical.updateFromParams(this.params);
            this.engine.particleSystem.updateFromController();
        });
        
        sameTypeControl.appendChild(visualizer);
        sameTypeControl.appendChild(sameTypeLabel);
        sameTypeControl.appendChild(sameTypeSlider);
        sameTypeControl.appendChild(sameTypeValueDisplay);
        
        this.biasPanel.appendChild(sameTypeControl);
        
        // Add controls for each relationship type
        ['orthogonal', 'diagonal', 'polar'].forEach(relType => {
            const control = document.createElement('div');
            control.style.marginBottom = '5px';
            
            // Create a visualizer showing which nodes have this relationship
            const nodeList = this.topical.getNodesWithRelationship(this.selectedType, relType);
            const visualizer = document.createElement('div');
            visualizer.style.display = 'flex';
            visualizer.style.gap = '5px';
            visualizer.style.marginBottom = '5px';
            
            nodeList.forEach(nodeType => {
                const node = document.createElement('span');
                node.textContent = nodeType.toUpperCase();
                node.style.width = '20px';
                node.style.height = '20px';
                node.style.borderRadius = '50%';
                node.style.backgroundColor = this.params.particleTypes[nodeType].color;
                node.style.color = this.getContrastColor(this.params.particleTypes[nodeType].color);
                node.style.display = 'flex';
                node.style.alignItems = 'center';
                node.style.justifyContent = 'center';
                node.style.fontSize = '10px';
                visualizer.appendChild(node);
            });
            
            const label = document.createElement('label');
            label.textContent = `${relType.charAt(0).toUpperCase() + relType.slice(1)} Bias: `;
            label.style.display = 'inline-block';
            label.style.width = '100px';
            
            const slider = document.createElement('input');
            slider.type = 'range';
            slider.min = -1;
            slider.max = 1;
            slider.step = 0.01;
            slider.value = this.params.particleTypes[this.selectedType][`${relType}Bias`];
            slider.style.width = '150px';
            slider.style.verticalAlign = 'middle';
            
            const valueDisplay = document.createElement('span');
            valueDisplay.textContent = slider.value;
            valueDisplay.style.display = 'inline-block';
            valueDisplay.style.width = '40px';
            valueDisplay.style.textAlign = 'right';
            
            slider.addEventListener('input', (e) => {
                this.params.particleTypes[this.selectedType][`${relType}Bias`] = parseFloat(e.target.value);
                valueDisplay.textContent = parseFloat(e.target.value).toFixed(2);
                
                // Force update all parameters
                this.topical.updateFromParams(this.params);
                this.engine.particleSystem.updateFromController();
                
                // Debug output
                console.log(`Set ${this.selectedType} ${relType} bias to ${e.target.value}`);
                console.log(`Affected nodes: ${nodeList.join(', ')}`);
            });
            
            control.appendChild(visualizer);
            control.appendChild(label);
            control.appendChild(slider);
            control.appendChild(valueDisplay);
            
            this.biasPanel.appendChild(control);
        });
        
        this.gui.__ul.appendChild(this.biasPanel);
    }

    updateSelectedTypeIndicator() {
        if (!this.biasPanel) return;
        
        const title = this.biasPanel.querySelector('div');
        if (!title) return;
        
        title.innerHTML = '';
        
        const nodeColor = document.createElement('span');
        nodeColor.style.display = 'inline-block';
        nodeColor.style.width = '20px';
        nodeColor.style.height = '20px';
        nodeColor.style.backgroundColor = this.params.particleTypes[this.selectedType].color;
        nodeColor.style.borderRadius = '50%';
        nodeColor.style.marginRight = '5px';
        nodeColor.style.verticalAlign = 'middle';
        
        title.appendChild(nodeColor);
        title.appendChild(document.createTextNode(`Node ${this.selectedType.toUpperCase()}`));
    }

    updateRelationships() {
        if (this.engine.particles) {
            this.engine.particles.updateFromController();
        }
    }
    
    getParticleTypeFromPosition(gridPosition) {
        return this.topical.getTypeFromPosition(gridPosition);
    }
    
    getAttractionValue(typeA, typeB) {
        return this.topical.getAttractionValue(typeA, typeB);
    }

    reset() {
        this.params.baseAttractions = {
            sameType: 0.7,
            orthogonal: 0.5,
            diagonal: 0.3,
            polar: 0.1
        };
        Object.values(this.params.particleTypes).forEach(type => {
            type.sameTypeBias = 0;
            type.orthogonalBias = 0;
            type.diagonalBias = 0;
            type.polarBias = 0;
        });
        this.updateRelationships();
    }

    getRelationshipType(typeA, typeB) {
        return this.topical.getRelationshipType(typeA, typeB);
    }

    getBinaryPosition(type) {
        return this.topical.getBinaryPosition(type);
    }

    getContrastColor(color) {
        // Implement your logic to determine a contrast color based on the input color
        // This is a placeholder and should be replaced with the actual implementation
        return '#000000'; // Placeholder return, actual implementation needed
    }

    highlightSelectedNode() {
        // Reset all nodes first
        Object.values(this.nodeElements).forEach(node => {
            const content = node.querySelector('.node-content');
            if (content) {
                content.style.boxShadow = '0 0 10px rgba(0,0,0,0.3)';
            }
        });
        
        // Highlight the selected node
        const selectedNode = this.nodeElements[this.selectedType];
        if (selectedNode) {
            const content = selectedNode.querySelector('.node-content');
            if (content) {
                content.style.boxShadow = '0 0 15px #fff, 0 0 10px #fff';
            }
        }
    }
}
