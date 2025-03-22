export default class Topical {
    constructor(params) {
        this.params = params;
        
        // Bit positions for each type
        this.bitPositions = {
            'a': [0, 0, 0],
            'b': [1, 0, 0],
            'c': [0, 1, 0],
            'd': [1, 1, 0],
            'e': [0, 0, 1],
            'f': [1, 0, 1],
            'g': [0, 1, 1],
            'h': [1, 1, 1]
        };
        
        // Create static relationship mappings based on binary distance
        this.relationshipMap = this.createRelationshipMap();
        
        // Cache for attraction values
        this.attractionCache = {};
        
        // Verify mappings
        this.validateRelationshipMappings();
    }
    
    createRelationshipMap() {
        // Pre-define all relationships in a static map
        const staticMap = {
            'a': {
                'a': 'sameType',
                'b': 'orthogonal', 'c': 'orthogonal', 'e': 'orthogonal',
                'd': 'diagonal', 'f': 'diagonal', 'g': 'diagonal',
                'h': 'polar'
            },
            'b': {
                'b': 'sameType',
                'a': 'orthogonal', 'd': 'orthogonal', 'f': 'orthogonal',
                'c': 'diagonal', 'e': 'diagonal', 'h': 'diagonal',
                'g': 'polar'
            },
            'c': {
                'c': 'sameType',
                'a': 'orthogonal', 'd': 'orthogonal', 'g': 'orthogonal',
                'b': 'diagonal', 'e': 'diagonal', 'h': 'diagonal',
                'f': 'polar'
            },
            'd': {
                'd': 'sameType',
                'b': 'orthogonal', 'c': 'orthogonal', 'h': 'orthogonal',
                'a': 'diagonal', 'f': 'diagonal', 'g': 'diagonal',
                'e': 'polar'
            },
            'e': {
                'e': 'sameType',
                'a': 'orthogonal', 'f': 'orthogonal', 'g': 'orthogonal',
                'b': 'diagonal', 'c': 'diagonal', 'h': 'diagonal',
                'd': 'polar'
            },
            'f': {
                'f': 'sameType',
                'b': 'orthogonal', 'e': 'orthogonal', 'h': 'orthogonal',
                'a': 'diagonal', 'd': 'diagonal', 'g': 'diagonal',
                'c': 'polar'
            },
            'g': {
                'g': 'sameType',
                'c': 'orthogonal', 'e': 'orthogonal', 'h': 'orthogonal',
                'a': 'diagonal', 'd': 'diagonal', 'f': 'diagonal',
                'b': 'polar'
            },
            'h': {
                'h': 'sameType',
                'd': 'orthogonal', 'f': 'orthogonal', 'g': 'orthogonal',
                'b': 'diagonal', 'c': 'diagonal', 'e': 'diagonal',
                'a': 'polar'
            }
        };
        
        return staticMap;
    }
    
    getTypeBits(type) {
        return this.bitPositions[type] || [0, 0, 0];
    }
    
    getRelationshipType(typeA, typeB) {
        return this.relationshipMap[typeA][typeB];
    }
    
    isRelationshipType(typeA, typeB, relationshipType) {
        return this.getRelationshipType(typeA, typeB) === relationshipType;
    }
    
    getAttractionValue(typeA, typeB) {
        const cacheKey = [typeA, typeB].sort().join('-');
        if (this.attractionCache[cacheKey] !== undefined) {
            return this.attractionCache[cacheKey];
        }
        
        const relType = this.getRelationshipType(typeA, typeB);
        const base = this.params.baseAttractions[relType];
        const biasA = this.params.particleTypes[typeA][`${relType}Bias`];
        const biasB = this.params.particleTypes[typeB][`${relType}Bias`];
        
        const value = base + biasA + biasB;
        
        this.attractionCache[cacheKey] = value;
        return value;
    }
    
    createTypeRelationshipMap() {
        const map = {};
        const types = ['a','b','c','d','e','f','g','h'];
        
        types.forEach(a => {
            map[a] = {};
            types.forEach(b => {
                map[a][b] = this.getAttractionValue(a, b);
            });
        });
        return map;
    }
    
    // Clear cache when attraction values are updated
    clearAttractionCache() {
        this.attractionCache = {};
    }
    
    // Update all values when parameters change
    updateFromParams(params) {
        this.params = params;
        this.clearAttractionCache();
    }
    
    // Get all nodes with specific relationship to a given node
    getNodesWithRelationship(node, relationshipType) {
        const types = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
        return types.filter(type => 
            type !== node && this.getRelationshipType(node, type) === relationshipType
        );
    }
    
    // Debugging: print all relationships for a node
    logNodeRelationships(nodeType) {
        console.log(`Relationships for node ${nodeType.toUpperCase()}:`);
        const types = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
        
        ['orthogonal', 'diagonal', 'polar'].forEach(relType => {
            const nodes = this.getNodesWithRelationship(nodeType, relType);
            console.log(`${relType}: ${nodes.map(n => n.toUpperCase()).join(', ')}`);
        });
    }

    // Helper method to verify our relationship mappings are correct
    validateRelationshipMappings() {
        // Polar relations (3 bits different)
        console.assert(this.getRelationshipType('a', 'h') === 'polar', "A-H should be polar");
        console.assert(this.getRelationshipType('e', 'd') === 'polar', "E-D should be polar");
        console.assert(this.getRelationshipType('f', 'c') === 'polar', "F-C should be polar");
        console.assert(this.getRelationshipType('g', 'b') === 'polar', "G-B should be polar");
        
        // Orthogonal relations (1 bit different)
        console.assert(this.getRelationshipType('a', 'b') === 'orthogonal', "A-B should be orthogonal");
        console.assert(this.getRelationshipType('a', 'c') === 'orthogonal', "A-C should be orthogonal");
        console.assert(this.getRelationshipType('a', 'e') === 'orthogonal', "A-E should be orthogonal");
        
        // Diagonal relations (2 bits different)
        console.assert(this.getRelationshipType('a', 'd') === 'diagonal', "A-D should be diagonal");
        console.assert(this.getRelationshipType('a', 'f') === 'diagonal', "A-F should be diagonal");
        console.assert(this.getRelationshipType('a', 'g') === 'diagonal', "A-G should be diagonal");
    }
}
