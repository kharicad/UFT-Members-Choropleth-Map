# Manhattan Schools UFT Members Interactive Choropleth Map 🗽📊

## Overview
An interactive choropleth map visualizing the distribution of United Federation of Teachers (UFT) members across Manhattan's NYC Department of Education schools. The map displays staff density through color gradients and provides detailed breakdowns of staff categories at each location.

<img width="720" height="789" alt="Screenshot 2025-07-24 at 11 37 48 AM" src="https://github.com/user-attachments/assets/6eb8cfa2-622b-4db1-be9a-56d1df67451d" />

## 🎯 Task
Create an interactive choropleth map representing all Manhattan schools with affiliated UFT members, showing:
- School locations with precise coordinates
- Total staff counts per school
- Breakdown by member types (active teachers, retirees, substitutes, etc.)
- Visual density representation through color and size

## 📊 Data Sources
- **schools.csv**: List of ~375 Manhattan schools (names and codes only)
- **school_members-1753196934512.csv**: Database of ~76,000 UFT members with school affiliations

## 🔧 Technical Process

### 1. **Geocoding Challenge**
The initial schools dataset lacked addresses and coordinates. To solve this:
- ❌ Manual Google searches (too time-consuming for 375 schools)
- ❌ ChatGPT address generation (inconsistent and error-prone)
- ✅ **API Solution**:
  - Primary: Nominatim (OpenStreetMap) API for bulk geocoding
  - Secondary: Google Maps API for missing addresses and verification
  - Result: `schoolsfinal_all_coordinates_updated.xlsx` with complete lat/long data

### 2. **Member Data Processing**
Processed 76,000 UFT members across 18 different categories:

#### Member Categories:
| Code | Description | Category |
|------|-------------|----------|
| ST | Staff W.F. and Union | Active |
| NT | Teachers & Pedagogues | Active |
| NP | Paraprofessionals | Active |
| RT, R7, RS, RB, RN, RV, ROTU | Various Retiree Types | Retired |
| PDF, PDO | Per Diem Staff | Per Diem |
| HG, LH, OTU, CO, VN, LRS | Administrative/Special | Other |

### 3. **Visualization Development**
Created an interactive map using Python's Folium library featuring:
- **Color gradient**: Gray (no data) → Yellow → Orange → Red (high density)
- **Dynamic sizing**: Circle radius proportional to staff count
- **Interactive popups**: Detailed staff breakdowns by category
- **Custom legend**: Real numbers instead of percentages

## 🚀 Features
- **Interactive Design**: Click any school for detailed staff composition
- **Multi-dimensional Data**: Shows both total counts and category breakdowns
- **Visual Hierarchy**: Larger, redder circles indicate higher staff density
- **Comprehensive Coverage**: All Manhattan DOE schools with UFT members

## 📁 Repository Structure
```
├── data/
│   ├── schools.csv                          # Original school list
│   ├── school_members-1753196934512.csv     # UFT member data
│   └── schoolsfinal_all_coordinates_updated.xlsx
├── scripts/
│   ├── geocode_missing_schools.py           # Geocoding script
│   ├── manhattan_schools_map.py             # Initial mapping
│   └── teacher_density_choropleth.py        # Final visualization
├── output/
│   ├── manhattan_schools_staff_interactive_map.html
│   ├── staff_distribution_analysis.txt
│   └── manhattan_schools_staff_summary.csv
└── README.md
```

## 🖥️ Usage
```bash
# Install dependencies
pip install pandas folium numpy openpyxl

# Run the visualization
python teacher_density_choropleth.py
```

## Key Findings
- **Total UFT members**: 75,911 across Manhattan schools
- **Retiree engagement**: Approximately 30% of members are retirees, showing strong post-career connections
- **Staff diversity**: 18 different member categories beyond traditional teachers
- **Density variation**: Staff counts range from 0 to 500+ per location
- **Substitute system**: Significant per diem workforce indicates robust coverage system

## 🛠️ Technologies Used
- **Python**: Data processing and visualization
- **Pandas**: Data manipulation
- **Folium**: Interactive map generation
- **APIs**: Nominatim & Google Maps for geocoding
- **HTML/CSS**: Custom styling for map elements

## 🔍 Possible Future Enhancements
- [ ] Add temporal analysis (member changes over time)
- [ ] Include salary/budget data visualization
- [ ] Expand to other NYC boroughs
- [ ] Add filtering options by member type

## BY:
Khari Cadogan

## 📄 License
N/A
---
*This project was created to visualize UFT member distribution across Manhattan schools, providing insights into staffing patterns and density across the NYC Department of Education.*
