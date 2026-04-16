"""
Inventory Visualizer Module
Handles data visualization for inventory system
"""
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List

class InventoryVisualizer:
    """Visualizes inventory data"""
    
    @staticmethod
    def create_inventory_pie_chart(equipment_list: List[Dict]):
        """Create pie chart of equipment by type"""
        
        type_distribution = {}
        for eq in equipment_list:
            eq_type = eq.get('type', 'Lainnya')
            if eq_type not in type_distribution:
                type_distribution[eq_type] = 0
            type_distribution[eq_type] += 1
        
        fig = go.Figure(data=[
            go.Pie(
                labels=list(type_distribution.keys()),
                values=list(type_distribution.values()),
                marker=dict(
                    colors=['#A5D6A7', '#90CAF9', '#FFE0B2', '#E1BEE7', '#F8BBD0']
                )
            )
        ])
        
        fig.update_layout(
            title="Equipment Distribution by Type",
            height=400,
            template="plotly_light"
        )
        
        return fig
    
    @staticmethod
    def create_value_distribution_chart(equipment_list: List[Dict]):
        """Create bar chart of equipment by total value"""
        
        # Top 10 most valuable equipment
        equipment_by_value = sorted(
            equipment_list,
            key=lambda x: float(x.get('harga_keseluruhan', 0)),
            reverse=True
        )[:10]
        
        names = [eq.get('nama', 'N/A')[:20] for eq in equipment_by_value]
        values = [float(eq.get('harga_keseluruhan', 0)) for eq in equipment_by_value]
        
        fig = go.Figure(data=[
            go.Bar(
                y=names,
                x=values,
                orientation='h',
                marker=dict(color='#66BB6A')
            )
        ])
        
        fig.update_layout(
            title="Top 10 Most Valuable Equipment",
            xaxis_title="Total Value (Rp)",
            yaxis_title="Equipment",
            height=400,
            template="plotly_light"
        )
        
        return fig
    
    @staticmethod
    def create_status_chart(equipment_list: List[Dict]):
        """Create status distribution chart"""
        
        status_count = {
            'active': 0,
            'maintenance': 0,
            'depleted': 0,
            'archived': 0
        }
        
        for eq in equipment_list:
            status = eq.get('status', 'active')
            if status in status_count:
                status_count[status] += 1
        
        status_labels = {
            'active': 'Aktif',
            'maintenance': 'Maintenance',
            'depleted': 'Habis Pakai',
            'archived': 'Diarsipkan'
        }
        
        labels = [status_labels.get(k, k) for k in status_count.keys()]
        values = list(status_count.values())
        
        colors = {
            'active': '#4CAF50',
            'maintenance': '#FFC107',
            'depleted': '#F44336',
            'archived': '#9E9E9E'
        }
        
        marker_colors = [colors.get(k, '#999') for k in status_count.keys()]
        
        fig = go.Figure(data=[
            go.Pie(
                labels=labels,
                values=values,
                marker=dict(colors=marker_colors)
            )
        ])
        
        fig.update_layout(
            title="Equipment Status Distribution",
            height=400,
            template="plotly_light"
        )
        
        return fig
    
    @staticmethod
    def create_lab_comparison_chart(labs_data: Dict):
        """Create lab equipment comparison chart"""
        
        lab_names = list(labs_data.keys())
        equipment_counts = [labs_data[lab].get('equipment_count', 0) for lab in lab_names]
        values = [labs_data[lab].get('total_value', 0) for lab in lab_names]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=lab_names,
            y=equipment_counts,
            name='Equipment Count',
            marker_color='#A5D6A7'
        ))
        
        fig.update_layout(
            title="Equipment Count per Lab",
            xaxis_title="Lab",
            yaxis_title="Count",
            height=400,
            template="plotly_light"
        )
        
        return fig
    
    @staticmethod
    def create_consumption_trend_chart(movements_data: List[Dict]):
        """Create consumption trend chart over time"""
        
        if not movements_data:
            return None
        
        # Group by date
        consumption_by_date = {}
        for m in movements_data:
            if m.get('movement_type') in ['out', 'adjustment']:
                date = m.get('date', '')[:10]
                if date not in consumption_by_date:
                    consumption_by_date[date] = 0
                consumption_by_date[date] += abs(m.get('quantity', 0))
        
        if not consumption_by_date:
            return None
        
        dates = sorted(consumption_by_date.keys())
        quantities = [consumption_by_date[d] for d in dates]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=quantities,
            mode='lines+markers',
            name='Consumption',
            line=dict(color='#EF5350', width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Equipment Consumption Trend",
            xaxis_title="Date",
            yaxis_title="Quantity",
            height=400,
            template="plotly_light"
        )
        
        return fig
    
    @staticmethod
    def create_category_breakdown_chart(equipment_list: List[Dict]):
        """Create equipment breakdown by category"""
        
        category_distribution = {}
        category_values = {}
        
        for eq in equipment_list:
            category = eq.get('kategori', 'Lainnya')
            qty = float(eq.get('jumlah', 0))
            value = float(eq.get('harga_keseluruhan', 0))
            
            if category not in category_distribution:
                category_distribution[category] = 0
                category_values[category] = 0
            
            category_distribution[category] += 1
            category_values[category] += value
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=list(category_distribution.keys()),
            y=list(category_distribution.values()),
            name='Count',
            marker_color='#A5D6A7'
        ))
        
        fig.update_layout(
            title="Equipment Distribution by Category",
            xaxis_title="Category",
            yaxis_title="Count",
            height=400,
            template="plotly_light"
        )
        
        return fig
