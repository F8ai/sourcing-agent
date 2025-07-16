"""
RDF/OWL Knowledge Base Parser
Handles semantic knowledge base operations for the sourcing agent
"""

import os
from typing import Dict, List, Any, Optional, Tuple
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, URIRef
from rdflib.namespace import XSD
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KnowledgeBase:
    """Manages the RDF/OWL knowledge base for sourcing information"""
    
    def __init__(self, knowledge_base_path: str = "rag/knowledge_base.ttl"):
        self.knowledge_base_path = knowledge_base_path
        self.graph = Graph()
        self.namespaces = {}
        self._load_knowledge_base()
    
    def _load_knowledge_base(self):
        """Load the RDF/OWL knowledge base from TTL file"""
        try:
            if os.path.exists(self.knowledge_base_path):
                self.graph.parse(self.knowledge_base_path, format="turtle")
                logger.info(f"Loaded knowledge base from {self.knowledge_base_path}")
                self._extract_namespaces()
            else:
                logger.warning(f"Knowledge base file not found: {self.knowledge_base_path}")
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")
    
    def _extract_namespaces(self):
        """Extract and store namespace information"""
        try:
            # Define expected namespaces
            expected_ns = {
                'sourcing': 'http://formul8.ai/ontology/sourcing#',
                'supplier': 'http://formul8.ai/ontology/supplier#',
                'cannabis': 'http://formul8.ai/ontology/cannabis#',
                'quality': 'http://formul8.ai/ontology/quality#',
                'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
                'owl': 'http://www.w3.org/2002/07/owl#',
                'xsd': 'http://www.w3.org/2001/XMLSchema#'
            }
            
            for prefix, uri in expected_ns.items():
                self.namespaces[prefix] = Namespace(uri)
                self.graph.bind(prefix, self.namespaces[prefix])
                
        except Exception as e:
            logger.error(f"Error extracting namespaces: {e}")
    
    def get_supplier_categories(self) -> List[Dict[str, Any]]:
        """Get all supplier categories from the knowledge base"""
        categories = []
        
        try:
            supplier_ns = self.namespaces.get('supplier')
            if not supplier_ns:
                return categories
            
            # Query for supplier types
            query = """
            SELECT ?category ?label ?products ?qualifications ?certifications ?services ?compliance
            WHERE {
                ?category a supplier:SupplierType .
                ?category rdfs:label ?label .
                OPTIONAL { ?category supplier:products ?products }
                OPTIONAL { ?category supplier:qualifications ?qualifications }
                OPTIONAL { ?category supplier:certifications ?certifications }
                OPTIONAL { ?category supplier:services ?services }
                OPTIONAL { ?category supplier:compliance ?compliance }
            }
            """
            
            results = self.graph.query(query)
            
            for row in results:
                category_info = {
                    'uri': str(row[0]),
                    'label': str(row[1]),
                    'products': self._parse_list_value(row[2]) if row[2] else [],
                    'qualifications': self._parse_list_value(row[3]) if row[3] else [],
                    'certifications': self._parse_list_value(row[4]) if row[4] else [],
                    'services': self._parse_list_value(row[5]) if row[5] else [],
                    'compliance': self._parse_list_value(row[6]) if row[6] else []
                }
                categories.append(category_info)
                
        except Exception as e:
            logger.error(f"Error getting supplier categories: {e}")
        
        return categories
    
    def get_quality_standards(self) -> List[Dict[str, Any]]:
        """Get quality standards from the knowledge base"""
        standards = []
        
        try:
            quality_ns = self.namespaces.get('quality')
            if not quality_ns:
                return standards
            
            # Query for quality standards
            query = """
            SELECT ?standard ?label ?criteria ?testing ?nutrients ?growing_media
            WHERE {
                ?standard a quality:Standard .
                ?standard rdfs:label ?label .
                OPTIONAL { ?standard quality:criteria ?criteria }
                OPTIONAL { ?standard quality:testing ?testing }
                OPTIONAL { ?standard quality:nutrients ?nutrients }
                OPTIONAL { ?standard quality:growing_media ?growing_media }
            }
            """
            
            results = self.graph.query(query)
            
            for row in results:
                standard_info = {
                    'uri': str(row[0]),
                    'label': str(row[1]),
                    'criteria': self._parse_list_value(row[2]) if row[2] else [],
                    'testing': self._parse_list_value(row[3]) if row[3] else [],
                    'nutrients': self._parse_list_value(row[4]) if row[4] else [],
                    'growing_media': self._parse_list_value(row[5]) if row[5] else []
                }
                standards.append(standard_info)
                
        except Exception as e:
            logger.error(f"Error getting quality standards: {e}")
        
        return standards
    
    def get_sourcing_strategies(self) -> List[Dict[str, Any]]:
        """Get sourcing strategies from the knowledge base"""
        strategies = []
        
        try:
            sourcing_ns = self.namespaces.get('sourcing')
            if not sourcing_ns:
                return strategies
            
            # Query for sourcing strategies
            query = """
            SELECT ?strategy ?label ?advantages ?challenges ?approach ?benefits ?scope ?considerations
            WHERE {
                ?strategy a sourcing:Strategy .
                ?strategy rdfs:label ?label .
                OPTIONAL { ?strategy sourcing:advantages ?advantages }
                OPTIONAL { ?strategy sourcing:challenges ?challenges }
                OPTIONAL { ?strategy sourcing:approach ?approach }
                OPTIONAL { ?strategy sourcing:benefits ?benefits }
                OPTIONAL { ?strategy sourcing:scope ?scope }
                OPTIONAL { ?strategy sourcing:considerations ?considerations }
            }
            """
            
            results = self.graph.query(query)
            
            for row in results:
                strategy_info = {
                    'uri': str(row[0]),
                    'label': str(row[1]),
                    'advantages': self._parse_list_value(row[2]) if row[2] else [],
                    'challenges': self._parse_list_value(row[3]) if row[3] else [],
                    'approach': self._parse_list_value(row[4]) if row[4] else [],
                    'benefits': self._parse_list_value(row[5]) if row[5] else [],
                    'scope': self._parse_list_value(row[6]) if row[6] else [],
                    'considerations': self._parse_list_value(row[7]) if row[7] else []
                }
                strategies.append(strategy_info)
                
        except Exception as e:
            logger.error(f"Error getting sourcing strategies: {e}")
        
        return strategies
    
    def get_supplier_assessment_criteria(self) -> Dict[str, Any]:
        """Get supplier assessment criteria and scoring weights"""
        assessment = {}
        
        try:
            sourcing_ns = self.namespaces.get('sourcing')
            if not sourcing_ns:
                return assessment
            
            # Query for supplier assessment process
            query = """
            SELECT ?process ?label ?criteria ?scoring_weights
            WHERE {
                ?process a sourcing:Process .
                ?process rdfs:label ?label .
                FILTER(CONTAINS(str(?label), "Assessment"))
                OPTIONAL { ?process sourcing:criteria ?criteria }
                OPTIONAL { ?process sourcing:scoring_weights ?scoring_weights }
            }
            """
            
            results = self.graph.query(query)
            
            for row in results:
                assessment = {
                    'uri': str(row[0]),
                    'label': str(row[1]),
                    'criteria': self._parse_list_value(row[2]) if row[2] else [],
                    'scoring_weights': self._parse_list_value(row[3]) if row[3] else []
                }
                break  # Should only be one assessment process
                
        except Exception as e:
            logger.error(f"Error getting supplier assessment criteria: {e}")
        
        return assessment
    
    def search_suppliers_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Search for suppliers by category"""
        categories = self.get_supplier_categories()
        return [cat for cat in categories if category.lower() in cat['label'].lower()]
    
    def search_quality_standards_by_type(self, standard_type: str) -> List[Dict[str, Any]]:
        """Search for quality standards by type"""
        standards = self.get_quality_standards()
        return [std for std in standards if standard_type.lower() in std['label'].lower()]
    
    def get_compliance_requirements(self) -> List[Dict[str, Any]]:
        """Get compliance requirements from the knowledge base"""
        requirements = []
        
        try:
            sourcing_ns = self.namespaces.get('sourcing')
            if not sourcing_ns:
                return requirements
            
            # Query for compliance requirements
            query = """
            SELECT ?regulation ?label ?regulations ?documentation
            WHERE {
                ?regulation a sourcing:Regulation .
                ?regulation rdfs:label ?label .
                OPTIONAL { ?regulation sourcing:regulations ?regulations }
                OPTIONAL { ?regulation sourcing:documentation ?documentation }
            }
            """
            
            results = self.graph.query(query)
            
            for row in results:
                requirement_info = {
                    'uri': str(row[0]),
                    'label': str(row[1]),
                    'regulations': self._parse_list_value(row[2]) if row[2] else [],
                    'documentation': self._parse_list_value(row[3]) if row[3] else []
                }
                requirements.append(requirement_info)
                
        except Exception as e:
            logger.error(f"Error getting compliance requirements: {e}")
        
        return requirements
    
    def _parse_list_value(self, value) -> List[str]:
        """Parse RDF list values into Python lists"""
        if not value:
            return []
        
        # Handle different types of list representations
        if isinstance(value, Literal):
            # Simple string that might contain comma-separated values
            text = str(value)
            if ',' in text:
                return [item.strip() for item in text.split(',')]
            else:
                return [text]
        elif isinstance(value, URIRef):
            # RDF list - would need more complex parsing
            return [str(value)]
        else:
            return [str(value)]
    
    def get_knowledge_base_summary(self) -> Dict[str, Any]:
        """Get a summary of the knowledge base contents"""
        return {
            'supplier_categories': len(self.get_supplier_categories()),
            'quality_standards': len(self.get_quality_standards()),
            'sourcing_strategies': len(self.get_sourcing_strategies()),
            'compliance_requirements': len(self.get_compliance_requirements()),
            'total_triples': len(self.graph),
            'namespaces': list(self.namespaces.keys())
        } 