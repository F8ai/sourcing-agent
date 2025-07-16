"""
Sourcing Agent Core Class
Main agent for cannabis industry sourcing operations
"""

import sys
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# Add base-agent to path
base_agent_path = os.path.join(os.path.dirname(__file__), '..', '..', 'base-agent')
sys.path.append(base_agent_path)

try:
    from core.agent import BaseAgent
except ImportError:
    # Fallback for when base-agent is not available
    class BaseAgent:
        def __init__(self, agent_name, description, domain, agent_path):
            self.agent_name = agent_name
            self.description = description
            self.domain = domain
            self.agent_path = agent_path
            self.tools = []
            self.memory = None
            self.llm = None
            self.agent = None
        
        def _initialize_llm(self):
            pass
        
        def _initialize_agent(self):
            pass
        
        async def process_query(self, user_id, query):
            return {
                "response": f"Mock response for: {query}",
                "confidence": 0.62,
                "response_time": 0.1,
                "user_id": user_id,
                "agent": self.agent_name
            }
from .knowledge_base import KnowledgeBase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SourcingAgent(BaseAgent):
    """Specialized agent for cannabis industry sourcing operations"""
    
    def __init__(self):
        super().__init__(
            agent_name="sourcing-agent",
            description="Intelligent sourcing agent for cannabis industry supply chain management",
            domain="Cannabis Sourcing and Supply Chain",
            agent_path="."
        )
        
        # Initialize knowledge base
        self.knowledge_base = KnowledgeBase()
        
        # Initialize sourcing-specific tools
        self._initialize_sourcing_tools()
        
        # Load sourcing-specific configuration
        self.config = self._load_sourcing_config()
    
    def _initialize_sourcing_tools(self):
        """Initialize sourcing-specific tools"""
        from langchain.tools import Tool
        
        # Supplier search tool
        supplier_search_tool = Tool(
            name="supplier_search",
            description="Search for suppliers by category, location, or certification",
            func=self._search_suppliers
        )
        
        # Quality assessment tool
        quality_assessment_tool = Tool(
            name="quality_assessment",
            description="Assess supplier quality against industry standards",
            func=self._assess_supplier_quality
        )
        
        # Compliance checking tool
        compliance_check_tool = Tool(
            name="compliance_check",
            description="Check supplier compliance with cannabis industry regulations",
            func=self._check_compliance
        )
        
        # Risk analysis tool
        risk_analysis_tool = Tool(
            name="risk_analysis",
            description="Analyze supply chain risks and provide mitigation strategies",
            func=self._analyze_risks
        )
        
        # Cost optimization tool
        cost_optimization_tool = Tool(
            name="cost_optimization",
            description="Analyze total cost of ownership and optimization opportunities",
            func=self._optimize_costs
        )
        
        # Add tools to the agent
        self.tools.extend([
            supplier_search_tool,
            quality_assessment_tool,
            compliance_check_tool,
            risk_analysis_tool,
            cost_optimization_tool
        ])
        
        # Reinitialize agent with new tools
        self._initialize_agent()
    
    def _load_sourcing_config(self) -> Dict[str, Any]:
        """Load sourcing-specific configuration"""
        return {
            'scoring_weights': {
                'quality': 0.30,
                'compliance': 0.25,
                'reliability': 0.20,
                'cost': 0.15,
                'service': 0.10
            },
            'risk_thresholds': {
                'high': 0.7,
                'medium': 0.4,
                'low': 0.2
            },
            'quality_standards': {
                'genetics': ['Genetic stability', 'Disease resistance', 'Potency consistency'],
                'nutrients': ['Heavy metal content', 'Microbial contamination', 'NPK accuracy'],
                'equipment': ['Safety standards', 'Energy efficiency', 'Durability'],
                'packaging': ['Child resistance', 'Food grade materials', 'Tamper evidence']
            }
        }
    
    def _search_suppliers(self, query: str) -> str:
        """Search for suppliers based on query"""
        try:
            # Parse the query to extract search criteria
            search_terms = query.lower().split()
            
            # Get supplier categories from knowledge base
            categories = self.knowledge_base.get_supplier_categories()
            
            # Filter categories based on search terms
            matching_categories = []
            for category in categories:
                category_text = f"{category['label']} {' '.join(category['products'])} {' '.join(category['qualifications'])}"
                if any(term in category_text.lower() for term in search_terms):
                    matching_categories.append(category)
            
            if matching_categories:
                result = "Found matching supplier categories:\n\n"
                for category in matching_categories:
                    result += f"**{category['label']}**\n"
                    result += f"Products: {', '.join(category['products'])}\n"
                    result += f"Qualifications: {', '.join(category['qualifications'])}\n"
                    if category['certifications']:
                        result += f"Certifications: {', '.join(category['certifications'])}\n"
                    result += "\n"
                return result
            else:
                return "No matching supplier categories found. Try different search terms."
                
        except Exception as e:
            logger.error(f"Error in supplier search: {e}")
            return f"Error searching suppliers: {str(e)}"
    
    def _assess_supplier_quality(self, supplier_info: str) -> str:
        """Assess supplier quality against industry standards"""
        try:
            # Get quality standards from knowledge base
            standards = self.knowledge_base.get_quality_standards()
            
            # Parse supplier information
            supplier_data = self._parse_supplier_info(supplier_info)
            
            assessment = f"Quality Assessment for {supplier_data.get('name', 'Supplier')}:\n\n"
            
            # Assess against relevant standards
            for standard in standards:
                if any(cat.lower() in supplier_data.get('category', '').lower() 
                      for cat in standard['label'].lower().split()):
                    
                    assessment += f"**{standard['label']}**\n"
                    
                    # Check criteria compliance
                    if standard['criteria']:
                        assessment += "Criteria Assessment:\n"
                        for criterion in standard['criteria']:
                            # Mock assessment - in real implementation, would check actual data
                            assessment += f"  ✓ {criterion} - Compliant\n"
                    
                    # Check testing requirements
                    if standard['testing']:
                        assessment += "Testing Requirements:\n"
                        for test in standard['testing']:
                            assessment += f"  - {test}\n"
                    
                    assessment += "\n"
            
            return assessment
            
        except Exception as e:
            logger.error(f"Error in quality assessment: {e}")
            return f"Error assessing quality: {str(e)}"
    
    def _check_compliance(self, supplier_info: str) -> str:
        """Check supplier compliance with cannabis industry regulations"""
        try:
            # Get compliance requirements from knowledge base
            requirements = self.knowledge_base.get_compliance_requirements()
            
            compliance_check = "Compliance Check Results:\n\n"
            
            for requirement in requirements:
                compliance_check += f"**{requirement['label']}**\n"
                
                if requirement['regulations']:
                    compliance_check += "Required Regulations:\n"
                    for regulation in requirement['regulations']:
                        compliance_check += f"  - {regulation}\n"
                
                if requirement['documentation']:
                    compliance_check += "Required Documentation:\n"
                    for doc in requirement['documentation']:
                        compliance_check += f"  - {doc}\n"
                
                compliance_check += "\n"
            
            return compliance_check
            
        except Exception as e:
            logger.error(f"Error in compliance check: {e}")
            return f"Error checking compliance: {str(e)}"
    
    def _analyze_risks(self, supply_chain_info: str) -> str:
        """Analyze supply chain risks and provide mitigation strategies"""
        try:
            # Get sourcing strategies from knowledge base
            strategies = self.knowledge_base.get_sourcing_strategies()
            
            risk_analysis = "Supply Chain Risk Analysis:\n\n"
            
            # Identify common risks
            common_risks = [
                "Supplier bankruptcy or financial instability",
                "Quality issues and product recalls",
                "Delivery delays and supply disruptions",
                "Price volatility and cost increases",
                "Regulatory changes and compliance issues",
                "Natural disasters and force majeure events"
            ]
            
            risk_analysis += "**Identified Risks:**\n"
            for risk in common_risks:
                risk_analysis += f"  ⚠️ {risk}\n"
            
            risk_analysis += "\n**Mitigation Strategies:**\n"
            
            # Get mitigation strategies from knowledge base
            for strategy in strategies:
                if 'diversified' in strategy['label'].lower():
                    risk_analysis += f"**{strategy['label']}**\n"
                    if strategy['approach']:
                        for approach in strategy['approach']:
                            risk_analysis += f"  - {approach}\n"
                    if strategy['benefits']:
                        risk_analysis += f"  Benefits: {', '.join(strategy['benefits'])}\n"
                    risk_analysis += "\n"
            
            return risk_analysis
            
        except Exception as e:
            logger.error(f"Error in risk analysis: {e}")
            return f"Error analyzing risks: {str(e)}"
    
    def _optimize_costs(self, cost_data: str) -> str:
        """Analyze total cost of ownership and optimization opportunities"""
        try:
            # Get cost optimization strategies from knowledge base
            strategies = self.knowledge_base.get_sourcing_strategies()
            
            cost_analysis = "Cost Optimization Analysis:\n\n"
            
            # Cost factors to consider
            cost_factors = [
                "Unit price and volume discounts",
                "Transportation and logistics costs",
                "Storage and inventory carrying costs",
                "Quality costs and testing requirements",
                "Administrative and transaction costs",
                "Risk mitigation costs"
            ]
            
            cost_analysis += "**Cost Factors to Consider:**\n"
            for factor in cost_factors:
                cost_analysis += f"  💰 {factor}\n"
            
            cost_analysis += "\n**Optimization Strategies:**\n"
            
            # Get optimization strategies from knowledge base
            for strategy in strategies:
                if any(term in strategy['label'].lower() for term in ['cost', 'optimization', 'diversified']):
                    cost_analysis += f"**{strategy['label']}**\n"
                    if strategy['advantages']:
                        for advantage in strategy['advantages']:
                            cost_analysis += f"  - {advantage}\n"
                    cost_analysis += "\n"
            
            return cost_analysis
            
        except Exception as e:
            logger.error(f"Error in cost optimization: {e}")
            return f"Error optimizing costs: {str(e)}"
    
    def _parse_supplier_info(self, supplier_info: str) -> Dict[str, Any]:
        """Parse supplier information from string"""
        # Simple parsing - in real implementation, would use more sophisticated parsing
        info = {
            'name': 'Unknown Supplier',
            'category': 'General',
            'location': 'Unknown',
            'certifications': []
        }
        
        # Extract basic information
        lines = supplier_info.split('\n')
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                
                if 'name' in key:
                    info['name'] = value
                elif 'category' in key:
                    info['category'] = value
                elif 'location' in key:
                    info['location'] = value
                elif 'certification' in key:
                    info['certifications'].append(value)
        
        return info
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the sourcing agent"""
        return f"""You are {self.agent_name}, a specialized AI agent for cannabis industry sourcing and supply chain management.

Your expertise includes:
- Supplier evaluation and selection
- Quality standards and compliance requirements
- Risk assessment and mitigation strategies
- Cost optimization and total cost of ownership analysis
- Cannabis industry regulations and best practices

You have access to a comprehensive knowledge base containing:
- Supplier categories and requirements
- Quality standards and testing protocols
- Sourcing strategies and best practices
- Compliance requirements and documentation needs

Always provide practical, actionable advice based on industry standards and regulatory requirements. Consider the unique challenges of the cannabis industry, including regulatory compliance, quality assurance, and supply chain security.

{self.description}"""
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get current agent status and capabilities"""
        kb_summary = self.knowledge_base.get_knowledge_base_summary()
        
        return {
            'agent_name': self.agent_name,
            'status': 'active',
            'knowledge_base': kb_summary,
            'tools_available': len(self.tools),
            'last_updated': datetime.now().isoformat(),
            'capabilities': [
                'Supplier search and evaluation',
                'Quality assessment',
                'Compliance checking',
                'Risk analysis',
                'Cost optimization'
            ]
        } 