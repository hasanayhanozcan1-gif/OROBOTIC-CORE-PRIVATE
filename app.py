"""
==============================================================================
PROJECT: OROBOTIC (ARMORED CORE)
OWNER: HASAN AYHAN ÖZCAN
STATUS: FAIL-SAFE MODE
==============================================================================
"""

import gradio as gr
import uuid
import hashlib
import datetime

# --- KİMYA MOTORU YÜKLEME DENEMESİ ---
# Eğer sunucu RDKit'i yükleyemezse sistem çökmez, "Metin Modu"na geçer.
try:
    from rdkit import Chem
    from rdkit.Chem import Descriptors
    CHEMISTRY_ACTIVE = True
except ImportError:
    CHEMISTRY_ACTIVE = False

# --- ÇEKİRDEK MANTIK ---
def run_system(smiles):
    # 1. KİMLİK OLUŞTURMA
    master_key = str(uuid.uuid4()).upper()[:12]
    mol_hash = hashlib.sha256(smiles.encode()).hexdigest()[:8]
    orb_address = f"orb://{mol_hash}.genesis"
    
    # 2. ANALİZ (HATA KORUMALI)
    if CHEMISTRY_ACTIVE:
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol:
                mw = Descriptors.MolWt(mol)
                power = min(100, (mw * 0.5) + 20)
                status_msg = "MOLECULAR ENGINE: ONLINE"
            else:
                power = 15.0
                status_msg = "INVALID MOLECULE (USING SIMULATION)"
        except:
            power = 10.0
            status_msg = "ENGINE ERROR (USING SIMULATION)"
    else:
        # Motor yüklenemediyse simülasyon verisi üret
        power = 99.9
        status_msg = "MOLECULAR ENGINE: OFFLINE (TEXT MODE)"

    nodes = int(power * 50000)
    
    # 3. GÖRSEL RAPOR (HTML)
    # Siyah-Beyaz Mimar Arayüzü
    html_report = f"""
    <div style='background: #000; border: 2px solid #fff; padding: 20px; color: #fff; font-family: monospace;'>
        <div style='border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 15px;'>
            <h2 style='margin:0; color:#fff;'>♔ THE ARCHITECT</h2>
            <div style='font-size:12px; color:#00ff00;'>OWNER: HASAN AYHAN ÖZCAN</div>
        </div>
        
        <div style='margin-bottom:15px; background:#111; padding:10px; border-left: 3px solid #00ff00;'>
            <div style='font-size:10px; color:#aaa;'>SYSTEM STATUS</div>
            <div style='font-size:14px; color:#fff;'>{status_msg}</div>
        </div>

        <div style='display:grid; grid-template-columns: 1fr 1fr; gap:10px; margin-bottom:15px;'>
            <div style='background:#111; padding:10px;'>
                <div style='font-size:10px; color:#aaa;'>GLOBAL NODES</div>
                <div style='font-size:18px; font-weight:bold;'>{nodes:,}</div>
            </div>
            <div style='background:#111; padding:10px;'>
                <div style='font-size:10px; color:#aaa;'>POWER</div>
                <div style='font-size:18px; font-weight:bold;'>{power:.1f}%</div>
            </div>
        </div>
        
        <div style='font-size:10px; color:#666; border-top:1px solid #333; padding-top:10px;'>
            ID: {master_key} <br>
            ADDR: {orb_address} <br>
            COPYRIGHT (C) 2026 HASAN AYHAN ÖZCAN
        </div>
    </div>
    """
    
    return html_report

# --- ARAYÜZ ---
css = """
body {background-color: #000; color: #fff;} 
.gradio-container {background-color: #000; border: none;} 
input {background-color: #222 !important; color: #fff !important; border: 1px solid #555 !important;}
button {background-color: #fff !important; color: #000 !important; font-weight: bold !important;}
"""

with gr.Blocks(css=css) as demo:
    gr.HTML("<h1 style='color:white; text-align:center; font-family:monospace;'>OROBOTIC GENESIS</h1>")
    
    with gr.Row():
        inp = gr.Textbox(label="SMILES CODE", value="C1=CC=C(C=C1)C=O")
        btn = gr.Button("INITIALIZE SYSTEM")
    
    out = gr.HTML(label="SYSTEM LOG")
    
    btn.click(run_system, inputs=inp, outputs=out)

if __name__ == "__main__":
    demo.launch()
