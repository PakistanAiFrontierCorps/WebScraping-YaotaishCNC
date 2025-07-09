# **Purpose and Scope**
This document provides a comprehensive overview of the WebScraping-YaotaishCNC system, a specialized web scraping solution designed to extract industrial automation product data from yaotaishcnc.com. The system focuses primarily on Fanuc brand components including AC spindle motors, controllers, and related industrial parts.

The system implements a multi-stage pipeline for URL collection, data extraction, processing, and output generation. It handles product attribute extraction including SKU numbers, titles, images, descriptions, and brand information, with robust error handling and data validation mechanisms.

For detailed information about individual scraping components, see Core Web Scraping System. For data processing workflows, see Data Processing Pipeline. For output management details, see Output Management and Data Storage.

# **System Architecture**
The WebScraping-YaotaishCNC system follows a layered architecture with distinct input, processing, and output components:

### System Architecture Overview
![image](https://github.com/user-attachments/assets/9eb5c337-c0f6-4706-a901-0ca2138ed84a)

# Core Components
### Primary Scraping Engine
The system's main scraping functionality is implemented in hello.ipynb, which serves as the primary data extraction engine:

### Core Scraping Process Flow
![image](https://github.com/user-attachments/assets/593a8168-5013-4723-bd39-b3b6d0c345a9)

### The scraper extracts specific product attributes using targeted CSS selectors:

*   Product titles via .jianjie em selector
*   Product images through .item-pic img elements
*   Descriptions from .jiann.mp sections
*   SKU extraction using regex pattern Module number[:：]?\s*([A-Za-z0-9\-/_.#]+)

![image](https://github.com/user-attachments/assets/cee4910c-f3ea-4a46-b4ba-ba171acf5678)

The system implements comprehensive data validation including:

*  Duplicate SKU detection using df.duplicated('SKU', keep=False)
*  Missing value validation with df['SKU'].isna().sum()
*  Data cleaning through df.dropna(subset=['SKU'])

## Data Flow Architecture

### Input Processing

The system begins with URL input from `input_urls.csv`, which contains target product pages.

| Input File      | Purpose         | Structure                              |
|-----------------|-----------------|----------------------------------------|
| `input_urls.csv` | URL source list | Single column `"Link"` with target URLs |

## Output Structure

The system generates standardized CSV outputs with a consistent schema:

| Field             | Description                   | Source                                  |
|------------------|-------------------------------|-----------------------------------------|
| `SKU`            | Product module number         | Regex extraction from description       |
| `Product Title`  | Product name                  | `.jianjie em` CSS selector              |
| `Images`         | Comma-separated image URLs    | `.item-pic img` elements                |
| `Description`    | Formatted product details     | `.jiann.mp` section processing          |
| `Short description` | Duplicate of description   | Same as description                     |
| `Brands`         | Product brand (typically "Fanuc") | Derived from description           |


## Key Implementation Details

### Web Scraping Configuration

The main scraper uses the following configuration:

## Key Implementation Details

### Web Scraping Configuration

The main scraper implements the following configuration:

```python
INPUT_CSV = "input_urls.csv"
OUTPUT_DIR = "Output CSV"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "products.csv")
BASE_URL = "https://www.yaotaishcnc.com/"
```
### Error Handling Strategy

The system implements robust error handling for failed requests:

- **Timeout**: Each request has a timeout configuration of **10 seconds**
- **Exception Handling**: All exceptions are caught and logged for debugging
- **Graceful Degradation**: In case of failure, the system inserts `"ERROR"` placeholder values into the output

# Data Quality Assurance
## Quality Control Workflow

![image](https://github.com/user-attachments/assets/ed59b10a-9593-4920-b2c7-120842c1447c)

he quality assurance process ensures data integrity through systematic validation and cleaning operations implemented in the utility notebooks.

## File Relationships and Dependencies

The system maintains clear separation of concerns across multiple file types:

- **Input Files**: CSV files containing URLs and configuration  
- **Processing Scripts**: Jupyter notebooks for scraping and data processing  
- **Output Files**: Generated CSV files with extracted product data  
- **Utility Scripts**: Validation and cleaning tools  

This architecture enables modular development, testing, and maintenance of the web scraping pipeline while ensuring robust data extraction and processing capabilities for industrial automation product catalogs.

