import matplotlib.pyplot as plt
import networkx as nx
import os
from typing import Dict, List

def create_degree_roadmap(courses: Dict, schedule: List[List[str]], output_path: str = "docs/degree_roadmap.png"):
    """Create a visual prerequisite graph with semester coloring."""
    G = nx.DiGraph()
    
    # Build graph from courses
    for course_id, info in courses.items():
        G.add_node(course_id, name=info['name'], credits=info['credits'])
        for prereq in info.get('prereqs', []):
            G.add_edge(prereq, course_id)
    
    # Layout: hierarchical based on schedule
    pos = nx.spring_layout(G, seed=42, k=2)
    
    plt.figure(figsize=(14, 10))
    
    # Color nodes by semester (green=early, blue=middle, red=late)
    node_colors = []
    for node in G.nodes():
        for sem_idx, semester in enumerate(schedule):
            if node in semester:
                if sem_idx < 2:
                    node_colors.append('#90EE90')  # Light green
                elif sem_idx >= len(schedule) - 2:
                    node_colors.append('#FFB6C1')  # Light red
                else:
                    node_colors.append('#ADD8E6')  # Light blue
                break
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2500, alpha=0.8)
    nx.draw_networkx_edges(G, pos, arrowsize=25, alpha=0.6, edge_color='gray', arrows=True)
    
    # Labels: Course ID + truncated name
    labels = {node: f"{node}\n{courses[node]['name'][:18]}..." for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
    
    plt.title("Degree Prerequisite Roadmap", fontsize=18, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    return output_path

def create_workload_chart(schedule: List[List[str]], courses: Dict, output_path: str = "docs/workload_chart.png"):
    """Create bar chart of credits per semester."""
    semester_nums = list(range(1, len(schedule) + 1))
    credits_per_semester = [sum(courses[c]['credits'] for c in sem) for sem in schedule]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(semester_nums, credits_per_semester, color='#4CAF50', alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Add credit labels on bars
    for bar, credits in zip(bars, credits_per_semester):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                str(credits), ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.xlabel('Semester', fontsize=12)
    plt.ylabel('Total Credits', fontsize=12)
    plt.title('Credit Load Distribution', fontsize=14, fontweight='bold')
    plt.xticks(semester_nums)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    return output_path