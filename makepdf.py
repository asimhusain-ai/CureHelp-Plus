import io
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle
from matplotlib.backends.backend_pdf import PdfPages

def generate_pdf_report(predictions, selected_diseases):
    COLORS = {
        'bg': '#f7f9fc',
        'text': '#333333',
        'header': '#0d47a1',
        'accent': '#1976d2',
        'low_risk': '#4caf50',
        'medium_risk': '#ff9800',
        'high_risk': '#d32f2f'
    }

    pdf_buffer = io.BytesIO()

    # Normalize selected_diseases
    if isinstance(selected_diseases, str):
        if selected_diseases.lower() in ['full report', 'all']:
            selected_diseases = list(predictions.keys())
        else:
            selected_diseases = [selected_diseases]

    # Filter predictions based on selection
    selected_predictions = {d: predictions[d] for d in selected_diseases if d in predictions}

    def _plot_gauge(ax, risk, color):
        ax.set_aspect('equal')
        ax.axis('off')
        ax.add_patch(Wedge((0, 0), 1, 0, 180, width=0.3, facecolor='#e0e0e0', alpha=0.7))
        ax.add_patch(Wedge((0, 0), 1, 180 - (risk / 100) * 180, 180, width=0.3, facecolor=color, alpha=1))
        ax.add_patch(Circle((0, 0), 0.7, facecolor='white'))
        ax.text(0, 0.15, f"{risk:.1f}%", ha='center', va='center', fontsize=20, fontweight='bold', color=color)
        ax.text(0, -0.05, "Risk Score", ha='center', va='center', fontsize=10, color='#555555')

    with PdfPages(pdf_buffer) as pdf:
        for disease, data in selected_predictions.items():
            inputs = data.get("inputs", {})
            risk = data.get("prob", 0)
            severity = data.get("severity", "N/A")

            risk_color = COLORS['high_risk'] if risk >= 75 else COLORS['medium_risk'] if risk > 40 else COLORS['low_risk']

            fig = plt.figure(figsize=(8.27, 11.69), facecolor=COLORS['bg'])
            fig.subplots_adjust(top=0.95, bottom=0.05)

            # Header
            ax_header = fig.add_axes([0.05, 0.91, 0.9, 0.08])
            ax_header.axis('off')
            ax_header.text(0.5, 0.6, "CureHelp+", ha='center', va='center', fontsize=22, fontweight='bold', color=COLORS['header'])
            ax_header.text(0.5, 0.2, "Disclaimer: This report is for informational purposes only. Always consult a doctor.", 
                           ha='center', va='center', fontsize=9, color='#555555', style='italic')

            ax_disease = fig.add_axes([0.05, 0.85, 0.9, 0.05])
            ax_disease.axis('off')
            disease_title = f"{disease} Risk"
            if severity != "N/A":
                disease_title += f" ({severity})"
            ax_disease.text(0.5, 0.5, disease_title, ha='center', va='center', fontsize=18, fontweight='bold', color=COLORS['accent'])

            # User inputs table
            ax_inputs = fig.add_axes([0.05, 0.55, 0.45, 0.28])
            ax_inputs.axis('off')
            if inputs:
                table_data = [[k, str(v)] for k, v in inputs.items()]
                table = ax_inputs.table(cellText=table_data, colLabels=['Parameter', 'Value'], loc='center', cellLoc='left', colWidths=[0.5, 0.5])
                table.auto_set_font_size(False)
                table.set_fontsize(9)
                table.scale(1, 1.5)
                for (row, col), cell in table.get_celld().items():
                    cell.set_edgecolor('#dddddd')
                    if row == 0:
                        cell.set_facecolor(COLORS['header'])
                        cell.set_text_props(weight='bold', color='white')
                    else:
                        cell.set_facecolor(COLORS['bg'] if row % 2 == 0 else '#ffffff')

            # Risk gauge
            ax_gauge = fig.add_axes([0.58, 0.55, 0.37, 0.28])
            _plot_gauge(ax_gauge, risk, risk_color)

            # Footer
            ax_footer = fig.add_axes([0.05, 0, 0.9, 0.02])
            ax_footer.axis('off')
            ax_footer.text(0.5, 0.5, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ha='center', va='center', fontsize=7, color='#888888')

            pdf.savefig(fig, facecolor=fig.get_facecolor())
            plt.close(fig)

    pdf_buffer.seek(0)
    return pdf_buffer