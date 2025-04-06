import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Sample Data (Replace with actual database data)
data = pd.DataFrame({
    "Skill": ["Python", "Java", "Angular", "Data Science"],
    "Users": [50, 40, 30, 25]
})

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1("SkillSync Dashboard"),
    # Skill Distribution Chart
    dcc.Graph(
        id="skill-chart",
        figure=px.bar(data, x="Skill", y="Users", title="User Skill Distribution")
    ),

    # Future Sections for Jobs & Courses
    html.Div("More Sections Coming Soon...")
])

if __name__ == "__main__":
    app.run_server(debug=True)
