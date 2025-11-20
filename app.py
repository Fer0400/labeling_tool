import streamlit as st
import pandas as pd
import io

# --- Configuration ---
st.set_page_config(page_title="Data Labeler", layout="wide")

# --- Constants --- CHECKED, ESTA BIEN!
DANGER_OPTIONS = sorted([
    'Activités Physiques', 'Agents biologiques', 'Ambiances thermiques', 'Bruit',
    'Chimiques', "Chutes d'objets", 'Chutes de hauteur', 'Chutes de plain pieds',
    "Chutes à l'eau", 'Circulation', 'Co-Activité', 'Eclairage', 'Effondrement',
    'Electricité', 'Elements sous pression', 'Ensevelissement', 'Equipement de travail',
    'Espace confinés', 'Facteurs humains', 'Incendie/Explosion', 'Manutention Mécaniques',
    'Poussières', 'Projections', 'Rayonnements', 'Risques Routiers', 'Stress',
    'Travail sur écran', 'Travailleurs isolés', 'Vibrations'
])

SEVERITY_OPTIONS = [1, 2, 3, 4, 5]

# --- Session State Initialization ---
if 'df' not in st.session_state:
    st.session_state.df = None
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

# --- Helper Functions ---
def load_data(file):
    try:
        df = pd.read_excel(file, engine='openpyxl')
        expected_cols = ['danger_1', 'danger_2', 'Severity_Score']
        for col in expected_cols:
            if col not in df.columns:
                df[col] = None
        
        # Auto-detect resume point
        missing_mask = df['danger_1'].isna() | (df['danger_1'].astype(str).str.strip() == '') | (df['danger_1'].astype(str).str.lower() == 'nan')
        missing_indices = df.index[missing_mask].tolist()
        start_idx = missing_indices[0] if missing_indices else 0
        
        return df, start_idx
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None, 0

def save_current_record(selected_dangers, severity):
    idx = st.session_state.current_index
    d1 = selected_dangers[0] if len(selected_dangers) > 0 else None
    d2 = selected_dangers[1] if len(selected_dangers) > 1 else None
    st.session_state.df.at[idx, 'danger_1'] = d1
    st.session_state.df.at[idx, 'danger_2'] = d2
    st.session_state.df.at[idx, 'Severity_Score'] = severity

def next_record():
    if st.session_state.current_index < len(st.session_state.df) - 1:
        st.session_state.current_index += 1

def prev_record():
    if st.session_state.current_index > 0:
        st.session_state.current_index -= 1

# --- Main App Layout ---
st.title("🛡️ Safety Incident Labeler")

if st.session_state.df is None:
    st.info("Upload your Excel file (.xlsx) to begin labeling.")
    uploaded_file = st.file_uploader("Choose an XLSX file", type=['xlsx'])
    if uploaded_file is not None:
        df, start_idx = load_data(uploaded_file)
        st.session_state.df = df
        st.session_state.current_index = start_idx
        if start_idx > 0:
             st.success(f"Welcome back! Resuming at record {start_idx + 1}.")
        st.rerun()
else:
    df = st.session_state.df
    total_records = len(df)
    if st.session_state.current_index >= total_records:
        st.session_state.current_index = total_records - 1
    current_idx = st.session_state.current_index
    row = df.iloc[current_idx]

    # --- Sidebar ---
    with st.sidebar:
        st.header("📍 Navigation")
        # Ensure Jump input doesn't reset unpredictably by using session state
        selected_idx = st.number_input("Jump to Record #", min_value=1, max_value=total_records, value=current_idx + 1, step=1)
        if selected_idx - 1 != st.session_state.current_index:
             st.session_state.current_index = selected_idx - 1
             st.rerun()

        st.progress((current_idx + 1) / total_records)
        st.write(f"Showing **{current_idx + 1}** of **{total_records}**")
        st.markdown("---")
        st.header("💾 File Operations")
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        st.download_button(
            label="Download Excel File",
            data=excel_buffer.getvalue(),
            file_name="labeled_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary"
        )

    # --- Main Area ---
    with st.expander("📋 Incident Metadata (Click to Expand/Collapse)", expanded=True):
        m1, m2 = st.columns([3, 1])
        with m1:
             st.write(f"**Description:** {row.get('Description', '')}")
        with m2:
             st.write(f"**Date:** {row.get('Date', 'N/A')}")
             st.write(f"**Location:** {row.get('Location', 'N/A')}")

    st.markdown("---")

    # --- Labeling Form ---
    st.subheader("🏷️ Apply Labels")
    
    with st.form("labeling_form", clear_on_submit=False):
        # 1. PREPARE DEFAULTS
        current_selections = []
        if pd.notna(row.get('danger_1')) and row['danger_1'] in DANGER_OPTIONS:
            current_selections.append(row['danger_1'])
        if pd.notna(row.get('danger_2')) and row['danger_2'] in DANGER_OPTIONS:
            current_selections.append(row['danger_2'])

        current_sev = row.get('Severity_Score', 1)
        try:
            sev_int = int(float(current_sev))
            sev_index = SEVERITY_OPTIONS.index(sev_int) if sev_int in SEVERITY_OPTIONS else 0
        except:
                sev_index = 0

        # 2. RENDER WIDGETS (With unique keys to force clearing on new records)
        st.write("**Select Dangers (1 Mandatory, max 2)**")
        # KEY CHANGE HERE: added key=f"pills_{current_idx}"
        dangers_input = st.pills(
            "Dangers",
            options=DANGER_OPTIONS,
            default=current_selections,
            selection_mode="multi",
            label_visibility="collapsed",
            key=f"pills_{current_idx}" 
        )

        st.markdown("---")
        c_sev, c_nav = st.columns([2, 3])
        with c_sev:
             # KEY CHANGE HERE: added key=f"sev_{current_idx}"
            sev_input = st.radio(
                "**Severity Score (1=Mineur, 2=Faible, 3=Modere, 4=Serieux, 5=Critique)**", 
                options=SEVERITY_OPTIONS, 
                index=sev_index,
                horizontal=True,
                key=f"sev_{current_idx}"
            )

        with c_nav:
            st.write("") # Spacer
            st.write("") # Spacer
            # 4-button layout
            b1, b2, b3, b4 = st.columns([1, 1, 1, 1.5])
            with b1: prev_submitted = st.form_submit_button("⬅️ Prev")
            with b2: skip_submitted = st.form_submit_button("⏭️ Skip")
            with b3: save_submitted = st.form_submit_button("💾 Save")
            with b4: next_submitted = st.form_submit_button("Save & Next ➡️", type="primary")

    # --- Submission Logic ---
    
    # VALIDATION FUNCTION
    def is_valid(dangers):
        if len(dangers) < 1:
            st.error("⚠️ Select at least one Danger.")
            return False
        elif len(dangers) > 2:
            st.error(f"⚠️ Too many selected ({len(dangers)}). Maximum is 2.")
            return False
        return True

    if next_submitted:
        if is_valid(dangers_input):
            save_current_record(dangers_input, sev_input)
            next_record()
            st.rerun()

    elif save_submitted:
        if is_valid(dangers_input):
            save_current_record(dangers_input, sev_input)
            st.success("✅ Record saved locally (don't forget to download eventually!)")
            # st.rerun is needed to update the sidebar progress if it changed from unlabelled to labelled
            st.rerun()
            
    elif skip_submitted:
        next_record()
        st.rerun()

    elif prev_submitted:
        # Optional: save before going back if valid
        if len(dangers_input) >= 1 and len(dangers_input) <= 2:
             save_current_record(dangers_input, sev_input)
        prev_record()
        st.rerun()