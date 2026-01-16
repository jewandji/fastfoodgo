import streamlit as st
import pandas as pd
import time
from fastfoodgo.database import get_db_connection
from fastfoodgo.seed import create_random_order
from fastfoodgo.agent import recommend

st.set_page_config(page_title="FastFoodGo Manager", page_icon="🍔", layout="wide")

st.title("FastFoodGo - Dashboard & IA")

# Menu Latéral
menu = st.sidebar.selectbox("Navigation", ["Commander (Simulation)", "Dashboard KPI", "Assistant IA"])

if menu == "Commander (Simulation)":
    st.header("Générateur de Commandes")
    st.write("Simulez l'activité du restaurant en générant des commandes aléatoires.")
    
    if st.button("Générer 1 commande"):
        conn = get_db_connection()
        create_random_order(conn)
        conn.close()
        st.success("Nouvelle commande créée avec succès !")
        
    if st.button("Mode Rush (Générer 10 commandes)"):
        conn = get_db_connection()
        progress_bar = st.progress(0)
        for i in range(10):
            create_random_order(conn)
            time.sleep(0.1)
            progress_bar.progress((i + 1) * 10)
        conn.close()
        st.success("Rush terminé ! 10 commandes ajoutées.")

elif menu == "Dashboard KPI":
    st.header("Analyse des Ventes")
    
    conn = get_db_connection()
    
    # KPIs en haut
    col1, col2, col3 = st.columns(3)
    
    # Requêtes SQL directes
    total_rev = pd.read_sql("SELECT SUM(total_price) FROM orders", conn).iloc[0,0]
    count_orders = pd.read_sql("SELECT COUNT(*) FROM orders", conn).iloc[0,0]
    
    with col1:
        st.metric("Chiffre d'Affaires", f"{total_rev:.2f} €" if total_rev else "0 €")
    with col2:
        st.metric("Total Commandes", count_orders)
        
    st.divider()
    
    # Graphiques
    col_graph1, col_graph2 = st.columns(2)
    
    with col_graph1:
        st.subheader("Ventes par Statut")
        df_status = pd.read_sql("SELECT status, count(*) as count FROM orders GROUP BY status", conn)
        st.bar_chart(df_status.set_index("status"))
        
    with col_graph2:
        st.subheader("Top Produits")
        query_top = """
            SELECT item_name, SUM(quantity) as qty 
            FROM order_items GROUP BY item_name ORDER BY qty DESC LIMIT 5
        """
        df_top = pd.read_sql(query_top, conn)
        st.dataframe(df_top, use_container_width=True)
        
    conn.close()
    
    if st.button("Rafraîchir les données"):
        st.rerun()

elif menu == "Assistant IA":
    st.header("Moteur de Recommandation")
    st.info("Testez le modèle d'IA entraîné pour faire du Cross-Selling.")
    
    # Choix du produit
    item = st.selectbox("Le client achète...", 
                        ["Burger Classique", "Cheese Royal", "Salade César", "Frites", "Soda"])
    
    if st.button("Demander à l'IA"):
        with st.spinner("L'IA réfléchit..."):
            reco = recommend(item)
        
        st.markdown(f"### Réponse de l'Agent :")
        st.success(reco)