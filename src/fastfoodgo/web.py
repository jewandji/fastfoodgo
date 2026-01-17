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
    st.header("📊 Cockpit de Pilotage")
    
    conn = get_db_connection()
    
    # --- 1. ACTIONS CUISINE (La solution à ton problème !) ---
    # On place ça en haut pour pouvoir agir vite
    st.markdown("### 👨‍🍳 Gestion de la Cuisine")
    col_action1, col_action2 = st.columns([3, 1])
    
    with col_action1:
        st.info("Les commandes s'accumulent ? Simulez le travail de l'équipe pour les expédier !")
        
    with col_action2:
        # Ce bouton va "traiter" les vieilles commandes
        if st.button("🔥 Traiter 5 commandes", type="primary"):
            cur = conn.cursor()
            # On prend les 5 plus vieilles commandes non livrées et on les passe en 'delivered'
            cur.execute("""
                UPDATE orders 
                SET status = 'delivered' 
                WHERE id IN (
                    SELECT id FROM orders 
                    WHERE status != 'delivered' 
                    ORDER BY id ASC 
                    LIMIT 5
                )
            """)
            conn.commit()
            cur.close()
            st.toast("5 commandes ont été servies ! 🚀", icon="🍔")
            time.sleep(1)
            st.rerun()

    st.markdown("---")

    # --- 2. CALCULS DES INDICATEURS (KPIs) ---
    df_metrics = pd.read_sql("SELECT SUM(total_price) as total, COUNT(*) as count FROM orders", conn)
    total_rev = df_metrics.iloc[0]['total']
    count_orders = df_metrics.iloc[0]['count']
    
    avg_basket = (total_rev / count_orders) if count_orders and count_orders > 0 else 0
    pending_orders = pd.read_sql("SELECT COUNT(*) FROM orders WHERE status != 'delivered'", conn).iloc[0,0]

    # --- 3. AFFICHAGE DES KPIS ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Chiffre d'Affaires", f"{total_rev:.2f} €" if total_rev else "0 €", "Cumulé")
    with col2:
        st.metric("Panier Moyen", f"{avg_basket:.2f} €")
    with col3:
        st.metric(
            "En Cuisine (En cours)", 
            pending_orders, 
            delta="-5" if st.session_state.get('last_action') == 'cook' else "À traiter",
            delta_color="inverse"
        )
        
    st.markdown("---")
    
    # --- 4. GRAPHIQUES ---
    col_graph1, col_graph2 = st.columns(2)
    
    with col_graph1:
        st.subheader("État des Commandes")
        df_status = pd.read_sql("SELECT status, count(*) as count FROM orders GROUP BY status", conn)
        st.bar_chart(df_status.set_index("status"), color="#FF4B4B")
        
    with col_graph2:
        st.subheader("🏆 Top Produits")
        query_top = """
            SELECT item_name, SUM(quantity) as qty 
            FROM order_items GROUP BY item_name ORDER BY qty DESC LIMIT 5
        """
        df_top = pd.read_sql(query_top, conn)
        st.bar_chart(df_top.set_index("item_name"), horizontal=True)
        
    # --- 5. DERNIÈRES VENTES ---
    st.subheader("🕒 Dernières Transactions")
    query_last = "SELECT id, created_at, status, total_price FROM orders ORDER BY id DESC LIMIT 5"
    df_last = pd.read_sql(query_last, conn)
    st.dataframe(df_last, use_container_width=True, hide_index=True)
    
    conn.close()

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