import pandas as pd
import folium
from folium import plugins
import numpy as np
import os
import sys

# checking for required files
required_files = {
    "schools": "schoolsfinal_all_coordinates_updated.xlsx",
    "teachers": "teacherslist.csv"
}

print("Checking for required files...")
for file_type, filename in required_files.items():
    if os.path.exists(filename):
        print(f"✓ Found {file_type} file: {filename}")
    else:
        print(f"✗ Missing {file_type} file: {filename}")
        print(f"  Please ensure {filename} is in the current directory: {os.getcwd()}")
        sys.exit(1)

# onloads the schools coordinates 
print("\nLoading school data...")
schools_df = pd.read_excel("schoolsfinal_all_coordinates_updated.xlsx")
print(f"Loaded {len(schools_df)} schools")

# onloads the teacher data
print("\nLoading teacher data...")
teachers_df = pd.read_csv("teacherslist.csv")
print(f"Loaded {len(teachers_df)} teacher records")

# counts off teachers by school_id
teacher_counts = teachers_df.groupby('school_id').size().reset_index(name='teacher_count')

# reveals the major statistics abt teacher data
print(f"\nTeacher data summary:")
print(f"Unique member groups: {teachers_df['member_group'].unique()}")
print(f"Number of schools with teachers: {len(teacher_counts)}")

# merges the teacher counts with school coordinates
schools_df['school_id_extracted'] = schools_df['school_id'].str.split(',').str[0].str.strip()

merged_df = schools_df.merge(teacher_counts, 
                             left_on='school_id_extracted', 
                             right_on='school_id', 
                             how='left')

# Fill NaN teacher counts with 0
merged_df['teacher_count'] = merged_df['teacher_count'].fillna(0).astype(int)

# Remove schools without coordinates
merged_df = merged_df.dropna(subset=['Latitude', 'Longitude'])

#  statistics for color scale
min_teachers = merged_df['teacher_count'].min()
max_teachers = merged_df['teacher_count'].max()
mean_teachers = merged_df['teacher_count'].mean()

#  breakpoints for legend using quintiles (20th, 40th, 60th, 80th percentiles)
teachers_with_count = merged_df[merged_df['teacher_count'] > 0]['teacher_count']
if len(teachers_with_count) > 0:
    breakpoint1 = int(teachers_with_count.quantile(0.2))
    breakpoint2 = int(teachers_with_count.quantile(0.4))
    breakpoint3 = int(teachers_with_count.quantile(0.6))
    breakpoint4 = int(teachers_with_count.quantile(0.8))
else:
    breakpoint1 = breakpoint2 = breakpoint3 = breakpoint4 = 0

print(f"\nTeacher count statistics:")
print(f"Min teachers per school: {min_teachers}")
print(f"Max teachers per school: {max_teachers}")
print(f"Mean teachers per school: {mean_teachers:.1f}")
print(f"Schools with no teachers: {len(merged_df[merged_df['teacher_count'] == 0])}")
print(f"\nColor breakpoints (quintiles):")
print(f"Light yellow: 1-{breakpoint1} teachers")
print(f"Yellow: {breakpoint1+1}-{breakpoint2} teachers")
print(f"Orange: {breakpoint2+1}-{breakpoint3} teachers")
print(f"Dark orange: {breakpoint3+1}-{breakpoint4} teachers")
print(f"Dark red: {breakpoint4+1}-{max_teachers} teachers")

# creates Manhattan centered map
print("\nCreating map...")
m = folium.Map(location=[40.7831, -73.9712], zoom_start=12)

# defines color numbers
def get_color(teacher_count):
    """Return color based on teacher count using actual thresholds"""
    if teacher_count == 0:
        return '#CCCCCC'  # Gray for schools with no teachers
    elif teacher_count <= breakpoint1:
        return '#FFEDA0'  # Light yellow
    elif teacher_count <= breakpoint2:
        return '#FED976'  # Yellow
    elif teacher_count <= breakpoint3:
        return '#FEB24C'  # Orange
    elif teacher_count <= breakpoint4:
        return '#FD8D3C'  # Dark orange
    else:
        return '#BD0026'  # Dark red

# defines radius function
def get_radius(teacher_count):
    """Return radius based on teacher count"""
    if teacher_count == 0:
        return 3
    return 3 + np.sqrt(teacher_count) * 0.5

# adds circles for each school
for idx, row in merged_df.iterrows():
    # popup text
    school_name = row.get('search_name', 'Unknown School')
    school_id = row.get('school_id_extracted', row.get('school_id', 'Unknown'))
    teacher_count = int(row['teacher_count'])
    
    popup_text = f"""
    <b>{school_name}</b><br>
    School ID: {school_id}<br>
    Teachers: {teacher_count}<br>
    """
    
    # Add circle marker
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=get_radius(teacher_count),
        popup=folium.Popup(popup_text, max_width=250),
        color='black',
        weight=1,
        fillColor=get_color(teacher_count),
        fillOpacity=0.7,
    ).add_to(m)

# creates custom legend with actual teacher counts and calculate breakpoints for legend
teachers_with_count = merged_df[merged_df['teacher_count'] > 0]['teacher_count']
if len(teachers_with_count) > 0:
    breakpoint1 = int(teachers_with_count.quantile(0.2))
    breakpoint2 = int(teachers_with_count.quantile(0.4))
    breakpoint3 = int(teachers_with_count.quantile(0.6))
    breakpoint4 = int(teachers_with_count.quantile(0.8))
else:
    breakpoint1 = breakpoint2 = breakpoint3 = breakpoint4 = 0

legend_html = f'''
<div style="position: fixed; 
            bottom: 50px; right: 50px; width: 200px; height: 220px; 
            background-color: white; border:2px solid grey; z-index:9999; 
            font-size:14px; padding: 10px">
<h4 style="margin-top:0;">UFT Member Count</h4>
<p style="margin: 5px;"><span style="background-color: #CCCCCC; padding: 3px;">&nbsp;&nbsp;&nbsp;</span> No teachers</p>
<p style="margin: 5px;"><span style="background-color: #FFEDA0; padding: 3px;">&nbsp;&nbsp;&nbsp;</span> 1 - {breakpoint1} teachers</p>
<p style="margin: 5px;"><span style="background-color: #FED976; padding: 3px;">&nbsp;&nbsp;&nbsp;</span> {breakpoint1+1} - {breakpoint2} teachers</p>
<p style="margin: 5px;"><span style="background-color: #FEB24C; padding: 3px;">&nbsp;&nbsp;&nbsp;</span> {breakpoint2+1} - {breakpoint3} teachers</p>
<p style="margin: 5px;"><span style="background-color: #FD8D3C; padding: 3px;">&nbsp;&nbsp;&nbsp;</span> {breakpoint3+1} - {breakpoint4} teachers</p>
<p style="margin: 5px;"><span style="background-color: #BD0026; padding: 3px;">&nbsp;&nbsp;&nbsp;</span> {breakpoint4+1} - {max_teachers} teachers</p>
<p style="margin: 5px; font-size: 12px;"><i>Circle size also indicates teacher count</i></p>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# title
title_html = '''
<div style="position: fixed; 
            top: 10px; left: 50%; transform: translateX(-50%); width: 400px;
            background-color: white; border:2px solid grey; z-index:9999; 
            font-size:16px; padding: 10px; text-align: center;">
<h3 style="margin: 0;">Manhattan Schools - Teacher Density Map</h3>
<p style="margin: 5px 0 0 0; font-size: 14px;">Active, Retired, Substitute, and All Teacher Types</p>
</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# save the map
output_filename = "manhattan_schools_teacher_choropleth.html"
m.save(output_filename)
print(f"\n✅ Map saved as {output_filename}")
print(f"   Full path: {os.path.abspath(output_filename)}")

# Create a summary report
summary_df = merged_df[merged_df['teacher_count'] > 0][['school_id_extracted', 'search_name', 'teacher_count']].sort_values('teacher_count', ascending=False)
print(f"\nTop 10 schools by teacher count:")
print(summary_df.head(10).to_string(index=False))

# Save summary statistics
summary_filename = "teacher_density_summary.txt"
with open(summary_filename, "w") as f:
    f.write("Manhattan Schools Teacher Density Analysis\n")
    f.write("=========================================\n\n")
    f.write(f"Total schools in dataset: {len(merged_df)}\n")
    f.write(f"Schools with teacher data: {len(merged_df[merged_df['teacher_count'] > 0])}\n")
    f.write(f"Schools without teacher data: {len(merged_df[merged_df['teacher_count'] == 0])}\n\n")
    f.write(f"Teacher Statistics:\n")
    f.write(f"- Total teachers: {merged_df['teacher_count'].sum()}\n")
    f.write(f"- Average teachers per school: {merged_df['teacher_count'].mean():.1f}\n")
    f.write(f"- Median teachers per school: {merged_df['teacher_count'].median():.1f}\n")
    f.write(f"- Max teachers at a school: {max_teachers}\n")
    f.write(f"- Min teachers at a school: {min_teachers}\n")

print(f"\n Summary statistics saved as {summary_filename}")
print(f"   Full path: {os.path.abspath(summary_filename)}")