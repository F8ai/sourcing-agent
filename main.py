#!/usr/bin/env python3
"""
Formul8 Sourcing Agent - Main Entry Point
Intelligent sourcing agent for cannabis industry supply chain management
"""

import os
import sys
import asyncio
import argparse
from typing import Dict, Any
import logging

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.sourcing_agent import SourcingAgent
# Add base-agent to path
base_agent_path = os.path.join(os.path.dirname(__file__), 'base-agent')
sys.path.append(base_agent_path)

try:
    from server import AgentServer
except ImportError:
    # Fallback for when base-agent is not available
    class AgentServer:
        def __init__(self, agent_name: str = "base-agent", port: int = 5000):
            self.agent_name = agent_name
            self.port = port
            self.app = None
        
        def run(self, debug: bool = False):
            print(f"Mock server for {self.agent_name} on port {self.port}")
            print("Base agent server not available - using mock implementation")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SourcingAgentServer(AgentServer):
    """Extended server for sourcing agent with additional endpoints"""
    
    def __init__(self, agent_name: str = "sourcing-agent", port: int = 5000):
        super().__init__(agent_name, port)
        self.sourcing_agent = SourcingAgent()
        self.setup_sourcing_routes()
    
    def setup_sourcing_routes(self):
        """Setup sourcing-specific routes"""
        
        @self.app.route('/api/supplier-categories')
        def get_supplier_categories():
            """Get all supplier categories from knowledge base"""
            try:
                categories = self.sourcing_agent.knowledge_base.get_supplier_categories()
                return self.app.jsonify(categories)
            except Exception as e:
                logger.error(f"Error getting supplier categories: {e}")
                return self.app.jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/quality-standards')
        def get_quality_standards():
            """Get quality standards from knowledge base"""
            try:
                standards = self.sourcing_agent.knowledge_base.get_quality_standards()
                return self.app.jsonify(standards)
            except Exception as e:
                logger.error(f"Error getting quality standards: {e}")
                return self.app.jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/sourcing-strategies')
        def get_sourcing_strategies():
            """Get sourcing strategies from knowledge base"""
            try:
                strategies = self.sourcing_agent.knowledge_base.get_sourcing_strategies()
                return self.app.jsonify(strategies)
            except Exception as e:
                logger.error(f"Error getting sourcing strategies: {e}")
                return self.app.jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/compliance-requirements')
        def get_compliance_requirements():
            """Get compliance requirements from knowledge base"""
            try:
                requirements = self.sourcing_agent.knowledge_base.get_compliance_requirements()
                return self.app.jsonify(requirements)
            except Exception as e:
                logger.error(f"Error getting compliance requirements: {e}")
                return self.app.jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/agent-status')
        def get_agent_status():
            """Get detailed agent status and capabilities"""
            try:
                status = self.sourcing_agent.get_agent_status()
                return self.app.jsonify(status)
            except Exception as e:
                logger.error(f"Error getting agent status: {e}")
                return self.app.jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/query', methods=['POST'])
        def process_query():
            """Process a sourcing query"""
            try:
                data = self.app.request.get_json()
                if not data or 'query' not in data:
                    return self.app.jsonify({'error': 'Query is required'}), 400
                
                user_id = data.get('user_id', 'anonymous')
                query = data['query']
                
                # Process query asynchronously
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(
                    self.sourcing_agent.process_query(user_id, query)
                )
                loop.close()
                
                return self.app.jsonify(response)
            except Exception as e:
                logger.error(f"Error processing query: {e}")
                return self.app.jsonify({'error': str(e)}), 500

        @self.app.route('/api/source-metrics')
        def get_source_metrics():
            """Get enhanced source metrics for dashboard"""
            import json
            import glob
            import os
            from datetime import datetime
            sources_file = os.path.join(os.path.dirname(__file__), 'sources', 'sources.json')
            metrics = {
                'total_sources': 0,
                'preferred_sources': 0,
                'states_covered': 0,
                'dispensaries': 0,
                'suppliers': 0,
                'manufacturers': 0,
                'testing_labs': 0,
                'recreational_medical': 0,
                'medical_only': 0,
                'last_scrape': None,
                'last_update': None,
                'preferred_sources_list': []
            }
            try:
                with open(sources_file, 'r') as f:
                    data = json.load(f)
                
                # Count preferred sources
                if data.get('preferred_sources'):
                    metrics['preferred_sources'] = len(data['preferred_sources'])
                    metrics['preferred_sources_list'] = data['preferred_sources']
                
                # Count sources by state and type
                total = metrics['preferred_sources']
                states = set()
                dispensaries = 0
                suppliers = 0
                manufacturers = 0
                testing_labs = 0
                recreational_medical = 0
                medical_only = 0
                
                if data.get('sources_by_state'):
                    for state, state_data in data['sources_by_state'].items():
                        states.add(state)
                        
                        # Count legal status
                        if state_data.get('legal_status') == 'recreational_medical':
                            recreational_medical += 1
                        elif state_data.get('legal_status') == 'medical_only':
                            medical_only += 1
                        
                        # Count dispensaries
                        if state_data.get('dispensaries'):
                            dispensaries += len(state_data['dispensaries'])
                            total += len(state_data['dispensaries'])
                        
                        # Count manufacturers
                        if state_data.get('manufacturers'):
                            manufacturers += len(state_data['manufacturers'])
                            total += len(state_data['manufacturers'])
                
                # Count national suppliers
                if data.get('national_suppliers'):
                    if data['national_suppliers'].get('equipment'):
                        suppliers += len(data['national_suppliers']['equipment'])
                        total += len(data['national_suppliers']['equipment'])
                    if data['national_suppliers'].get('packaging'):
                        suppliers += len(data['national_suppliers']['packaging'])
                        total += len(data['national_suppliers']['packaging'])
                    if data['national_suppliers'].get('testing'):
                        testing_labs += len(data['national_suppliers']['testing'])
                        total += len(data['national_suppliers']['testing'])
                
                # Count consulting services
                if data.get('consulting_services'):
                    suppliers += len(data['consulting_services'])
                    total += len(data['consulting_services'])
                
                metrics['total_sources'] = total
                metrics['states_covered'] = len(states)
                metrics['dispensaries'] = dispensaries
                metrics['suppliers'] = suppliers
                metrics['manufacturers'] = manufacturers
                metrics['testing_labs'] = testing_labs
                metrics['recreational_medical'] = recreational_medical
                metrics['medical_only'] = medical_only
                metrics['last_update'] = data.get('metadata', {}).get('last_updated', 'Unknown')
                
            except Exception as e:
                metrics['error'] = str(e)
            
            # Find last scrape file
            try:
                scrape_files = glob.glob(os.path.join(os.path.dirname(__file__), 'sources', 'scraped_data_*.json'))
                if scrape_files:
                    latest = max(scrape_files, key=os.path.getmtime)
                    ts = os.path.getmtime(latest)
                    metrics['last_scrape'] = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
            except Exception as e:
                metrics['last_scrape'] = None
            
            return self.app.jsonify(metrics)

def run_cli_mode():
    """Run the sourcing agent in CLI mode"""
    agent = SourcingAgent()
    
    print("🌿 Formul8 Sourcing Agent - CLI Mode")
    print("=" * 50)
    print("Type 'help' for available commands, 'quit' to exit")
    print()
    
    while True:
        try:
            user_input = input("sourcing-agent> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break
            elif user_input.lower() == 'help':
                print_help()
            elif user_input.lower() == 'status':
                status = agent.get_agent_status()
                print_agent_status(status)
            elif user_input.lower() == 'categories':
                categories = agent.knowledge_base.get_supplier_categories()
                print_supplier_categories(categories)
            elif user_input.lower() == 'standards':
                standards = agent.knowledge_base.get_quality_standards()
                print_quality_standards(standards)
            elif user_input.lower() == 'strategies':
                strategies = agent.knowledge_base.get_sourcing_strategies()
                print_sourcing_strategies(strategies)
            elif user_input.lower() == 'compliance':
                requirements = agent.knowledge_base.get_compliance_requirements()
                print_compliance_requirements(requirements)
            elif user_input:
                # Process as a query
                print("Processing query...")
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(
                    agent.process_query('cli_user', user_input)
                )
                loop.close()
                
                print(f"\nResponse: {response['response']}")
                print(f"Confidence: {response['confidence']:.2f}")
                print(f"Response Time: {response['response_time']:.2f}s")
                print()
            else:
                continue
                
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            logger.error(f"Error in CLI mode: {e}")
            print(f"Error: {e}")

def print_help():
    """Print help information"""
    print("\nAvailable Commands:")
    print("  help        - Show this help message")
    print("  status      - Show agent status and capabilities")
    print("  categories  - List supplier categories")
    print("  standards   - List quality standards")
    print("  strategies  - List sourcing strategies")
    print("  compliance  - List compliance requirements")
    print("  quit/exit/q - Exit the application")
    print("\nOr simply type your sourcing question!")
    print()

def print_agent_status(status: Dict[str, Any]):
    """Print agent status in a formatted way"""
    print(f"\n🤖 Agent Status:")
    print(f"  Name: {status['agent_name']}")
    print(f"  Status: {status['status']}")
    print(f"  Tools Available: {status['tools_available']}")
    print(f"  Last Updated: {status['last_updated']}")
    
    print(f"\n📚 Knowledge Base:")
    kb = status['knowledge_base']
    print(f"  Supplier Categories: {kb['supplier_categories']}")
    print(f"  Quality Standards: {kb['quality_standards']}")
    print(f"  Sourcing Strategies: {kb['sourcing_strategies']}")
    print(f"  Compliance Requirements: {kb['compliance_requirements']}")
    print(f"  Total Triples: {kb['total_triples']}")
    
    print(f"\n🛠️ Capabilities:")
    for capability in status['capabilities']:
        print(f"  • {capability}")
    print()

def print_supplier_categories(categories: list):
    """Print supplier categories in a formatted way"""
    print(f"\n🏗️ Supplier Categories ({len(categories)}):")
    for category in categories:
        print(f"\n  📋 {category['label']}")
        if category['products']:
            print(f"     Products: {', '.join(category['products'])}")
        if category['qualifications']:
            print(f"     Qualifications: {', '.join(category['qualifications'])}")
        if category['certifications']:
            print(f"     Certifications: {', '.join(category['certifications'])}")
    print()

def print_quality_standards(standards: list):
    """Print quality standards in a formatted way"""
    print(f"\n📊 Quality Standards ({len(standards)}):")
    for standard in standards:
        print(f"\n  ✅ {standard['label']}")
        if standard['criteria']:
            print(f"     Criteria: {', '.join(standard['criteria'])}")
        if standard['testing']:
            print(f"     Testing: {', '.join(standard['testing'])}")
    print()

def print_sourcing_strategies(strategies: list):
    """Print sourcing strategies in a formatted way"""
    print(f"\n🎯 Sourcing Strategies ({len(strategies)}):")
    for strategy in strategies:
        print(f"\n  🎯 {strategy['label']}")
        if strategy['advantages']:
            print(f"     Advantages: {', '.join(strategy['advantages'])}")
        if strategy['benefits']:
            print(f"     Benefits: {', '.join(strategy['benefits'])}")
    print()

def print_compliance_requirements(requirements: list):
    """Print compliance requirements in a formatted way"""
    print(f"\n⚖️ Compliance Requirements ({len(requirements)}):")
    for requirement in requirements:
        print(f"\n  📋 {requirement['label']}")
        if requirement['regulations']:
            print(f"     Regulations: {', '.join(requirement['regulations'])}")
        if requirement['documentation']:
            print(f"     Documentation: {', '.join(requirement['documentation'])}")
    print()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Formul8 Sourcing Agent - Cannabis Industry Supply Chain Management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Start web server
  python main.py --cli              # Start CLI mode
  python main.py --port 8080        # Start server on port 8080
  python main.py --query "Find genetics suppliers"  # Process single query
        """
    )
    
    parser.add_argument(
        '--cli',
        action='store_true',
        help='Run in CLI mode instead of web server'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Port for web server (default: 5000)'
    )
    
    parser.add_argument(
        '--query',
        type=str,
        help='Process a single query and exit'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    args = parser.parse_args()
    
    # Set debug level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        if args.query:
            # Process single query
            agent = SourcingAgent()
            print(f"Processing query: {args.query}")
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(
                agent.process_query('cli_user', args.query)
            )
            loop.close()
            
            print(f"\nResponse: {response['response']}")
            print(f"Confidence: {response['confidence']:.2f}")
            print(f"Response Time: {response['response_time']:.2f}s")
            
        elif args.cli:
            # Run in CLI mode
            run_cli_mode()
        else:
            # Run web server
            server = SourcingAgentServer(port=args.port)
            print(f"🌿 Starting Formul8 Sourcing Agent on http://0.0.0.0:{args.port}")
            print(f"📊 Dashboard: http://localhost:{args.port}")
            print(f"🔧 API: http://localhost:{args.port}/api")
            print("Press Ctrl+C to stop")
            server.run(debug=args.debug)
            
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        logger.error(f"Error in main: {e}")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 