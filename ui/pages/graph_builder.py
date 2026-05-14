import streamlit as st
import streamlit.components.v1 as components


def render_graph_builder():
    st.title("🕸️ Graph Builder")

    html_code = """
    <html>
    <head>
    <style>
        body {
            margin: 0;
            background: #0f172a;
            color: white;
            font-family: Arial;
        }

        .container {
            display: flex;
            height: 600px;
        }

        .sidebar, .chat {
            width: 20%;
            padding: 20px;
            background: #1e293b;
        }

        .canvas {
            flex: 1;
            position: relative;
            background: #111827;
        }

        .node {
            position: absolute;
            padding: 12px 20px;
            border-radius: 12px;
            font-weight: bold;
        }

        .ventas { top: 80px; left: 80px; background: #2563eb; }
        .clientes { top: 80px; right: 80px; background: #059669; }
        .campañas { bottom: 80px; left: 40%; background: #7c3aed; }
    </style>
    </head>
    <body>
        <div class="container">
            <div class="sidebar">
                <h3>Datasets</h3>
                <p>ventas.csv</p>
                <p>clientes.csv</p>
                <p>campañas.csv</p>
            </div>

            <div class="canvas">
                <div class="node ventas">ventas</div>
                <div class="node clientes">clientes</div>
                <div class="node campañas">campañas</div>
            </div>

            <div class="chat">
                <h3>AI Chat</h3>
                <p>ventas por cliente y campaña</p>
            </div>
        </div>
    </body>
    </html>
    """

    components.html(html_code, height=600)