# Formul8 Sourcing Agent

An intelligent sourcing agent designed for the cannabis industry, helping organizations identify, evaluate, and manage suppliers across the entire supply chain.

## Overview

The Formul8 Sourcing Agent is an AI-powered tool that leverages semantic knowledge to assist cannabis businesses in making informed sourcing decisions. It provides comprehensive guidance on supplier evaluation, quality standards, compliance requirements, and strategic sourcing approaches.

## Features

### 🏗️ Supplier Categories
- **Genetics Suppliers**: Seeds, clones, mother plants, tissue culture
- **Nutrient Suppliers**: Base nutrients, micronutrients, pH adjusters, growth stimulants
- **Equipment Suppliers**: LED lighting, HVAC, irrigation, environmental controllers
- **Packaging Suppliers**: Child-resistant containers, labels, exit bags

### 📊 Quality Standards
- **Genetics Quality**: Genetic stability, disease resistance, potency consistency
- **Input Material Quality**: Heavy metal content, microbial contamination, NPK accuracy
- **Compliance Standards**: State regulations, testing requirements, documentation

### 🎯 Sourcing Strategies
- **Local Sourcing**: Reduced costs, faster delivery, local economy support
- **Diversified Sourcing**: Multiple suppliers, geographic diversification, risk mitigation
- **Vertical Integration**: In-house operations, increased control, quality assurance

### ⚖️ Supplier Evaluation
- **Assessment Criteria**: Quality certifications, regulatory compliance, financial stability
- **Scoring Weights**: Quality (30%), Compliance (25%), Reliability (20%), Cost (15%), Service (10%)
- **Performance Metrics**: On-time delivery, quality acceptance, customer service rating

### 🔒 Risk Management
- **Supply Chain Risks**: Supplier bankruptcy, quality issues, delivery delays
- **Mitigation Strategies**: Supplier diversification, quality audits, contingency planning
- **Compliance Requirements**: Licensed supplier verification, seed-to-sale tracking

## Base Agent Integration

This project integrates with the **base-agent** submodule, which provides shared functionality for all Formul8 agents:

### Core Features
- **BaseAgent Class**: Common agent functionality and LangChain integration
- **Web Dashboard**: Flask-based monitoring interface with metrics and status
- **Tool Framework**: Extensible tool system for specialized agent capabilities
- **Memory Management**: Conversation history and context preservation
- **Error Handling**: Robust error handling and fallback mechanisms

### Integration Benefits
- **Consistent Architecture**: All Formul8 agents share the same base structure
- **Shared Components**: Common utilities, monitoring, and dashboard features
- **Easy Development**: Inherit from BaseAgent class for rapid development
- **Standardized APIs**: Consistent interface across all specialized agents

## Sources Collection

The sourcing agent maintains a comprehensive database of cannabis industry suppliers organized by state and category:

### Source Categories
- **Preferred Sources**: Featured suppliers with proven track records (e.g., Extract Consultants)
- **Materials Suppliers**: Genetics, nutrients, packaging, and growing media
- **Equipment Suppliers**: Lighting, HVAC, irrigation, environmental controls
- **National Suppliers**: Companies serving multiple states or nationwide
- **State-Specific Suppliers**: Local suppliers organized by legal cannabis states

### Current Coverage
- **69 Total Sources** across 20+ legal cannabis states
- **Preferred Sources**: 1 (Extract Consultants)
- **Materials Suppliers**: Genetics, nutrients, packaging, growing media
- **Equipment Suppliers**: Lighting, ventilation, environmental controls, grow systems

### Source Data Structure
Each source includes:
- Company name and website URL
- Category and product offerings
- Location and service areas
- Preferred status indicator
- Contact information (when available)
- Certifications and compliance information

### Web Scraping Capabilities
The agent includes a sophisticated web scraper (`scrape_sources.py`) that can:
- Extract product information from supplier websites
- Collect contact information and locations
- Identify certifications and compliance details
- Rate-limit requests to be respectful to websites
- Save structured data for agent use

### Usage
```bash
# View all sources without scraping
python scrape_sources.py --dry-run

# Scrape all sources
python scrape_sources.py

# Scrape with custom settings
python scrape_sources.py --max-concurrent 3 --output results.json
```

## Knowledge Base

The agent uses a comprehensive RDF/OWL knowledge base (`rag/knowledge_base.ttl`) that includes:

- **Ontology Definitions**: Structured data models for suppliers, quality, and sourcing
- **Supplier Types**: Detailed categorization of cannabis industry suppliers
- **Quality Standards**: Industry-specific quality criteria and testing requirements
- **Sourcing Processes**: Step-by-step approaches for supplier evaluation and selection
- **Compliance Framework**: Regulatory requirements and documentation needs

## Installation

### Prerequisites
- Python 3.8+
- GitHub CLI (for issue tracking and collaboration)

### Setup
```bash
# Clone the repository with submodules
git clone --recursive https://github.com/F8ai/sourcing-agent.git
cd sourcing-agent

# Or if already cloned, initialize and update submodules
git submodule init
git submodule update

# Install GitHub CLI (if not already installed)
brew install gh

# Authenticate with GitHub
gh auth login

# Install Python dependencies (when available)
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
# Start the sourcing agent
python main.py

# Query supplier information
python agent.py --query "Find genetics suppliers in California"

# Evaluate supplier quality
python agent.py --evaluate --supplier "ABC Genetics"
```

### Advanced Features
- **Supplier Search**: Find suppliers by category, location, and certification
- **Quality Assessment**: Evaluate suppliers against industry standards
- **Risk Analysis**: Identify and mitigate supply chain risks
- **Compliance Checking**: Verify regulatory compliance requirements
- **Cost Optimization**: Analyze total cost of ownership and optimization opportunities

## Project Structure

```
sourcing-agent/
├── base-agent/               # Base agent submodule (shared functionality)
│   ├── core/
│   │   └── agent.py         # Base agent class and shared tools
│   ├── templates/
│   │   └── dashboard.html   # Web dashboard template
│   └── server.py            # Flask web server for agent monitoring
├── sources/                  # Cannabis industry sources collection
│   └── sources.json         # Comprehensive supplier database by state
├── rag/
│   └── knowledge_base.ttl    # Semantic knowledge base
├── src/                      # Source code
│   ├── core/                # Core agent functionality
│   │   ├── knowledge_base.py # RDF/OWL knowledge base parser
│   │   └── sourcing_agent.py # Main sourcing agent class
│   ├── utils/               # Utility modules
│   │   └── scraper.py       # Web scraper for supplier data
│   ├── tools/               # Agent tools (to be implemented)
│   ├── api/                 # API endpoints (to be implemented)
│   └── __init__.py          # Package initialization
├── tests/                    # Test suite (to be implemented)
├── docs/                     # Documentation (to be implemented)
├── .gitmodules              # Git submodule configuration
├── main.py                   # Main entry point
├── scrape_sources.py         # Source scraping CLI tool
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Development Roadmap

### Phase 1: Core Infrastructure
- [ ] Implement RDF/OWL knowledge base parser
- [ ] Create supplier search and evaluation engine
- [ ] Develop quality assessment algorithms
- [ ] Build compliance checking system

### Phase 2: Advanced Features
- [ ] Risk assessment and mitigation tools
- [ ] Cost optimization analysis
- [ ] Supplier performance tracking
- [ ] Automated supplier recommendations

### Phase 3: Integration & Scale
- [ ] API development for external integrations
- [ ] Web interface for non-technical users
- [ ] Mobile application for field use
- [ ] Advanced analytics and reporting

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow semantic web standards for knowledge base updates
- Maintain comprehensive test coverage
- Document all new features and APIs
- Ensure compliance with cannabis industry regulations

## License

This project is proprietary software developed by Formul8 (F8ai). All rights reserved.

## Support

For support and questions:
- Create an issue in this repository
- Contact the Formul8 development team
- Check the documentation in the `docs/` directory

## Compliance Notice

This software is designed to assist with cannabis industry sourcing decisions. Users are responsible for ensuring compliance with all applicable local, state, and federal regulations. The software does not guarantee regulatory compliance and should be used in conjunction with proper legal and compliance review.

---

**Formul8 Sourcing Agent** - Intelligent sourcing solutions for the cannabis industry. 