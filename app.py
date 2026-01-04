"""
==============================================================================
PROJECT: OROBOTIC (THE ARCHITECT EDITION)
OWNER & FOUNDER: HASAN AYHAN ÖZCAN
DATE: 2026-01-04
LICENSE: PROPRIETARY / COPYRIGHT PROTECTED
STATUS: MASTER NODE (ROOT) - GLOBAL STABLE BUILD
==============================================================================
"""
async def execute(smiles, language):
    loop = asyncio.get_running_loop()
    block, report = await loop.run_in_executor(None, functools.partial(run_architect_core, smiles, language))
    if block is None: return None, report
    
    # Unique ID for the viewer instance
    unique_id = f"mol_view_{uuid.uuid4().hex[:8]}"
    
    # Enhanced 3D visualization settings
    view = py3Dmol.view(width="100%", height="500px")
    view.addModel(block, 'mol')
    view.setStyle({'stick': {'radius': 0.2, 'colorscheme': 'cyanCarbon'}, 
                   'sphere': {'scale': 0.3}})
    view.setBackgroundColor('#000000')
    view.zoomTo()
    view.spin(True)
    
    # Extracting the HTML/JS component specifically
    mol_html = view._make_html()
    
    # Wrapping in a stable container for Gradio gr.HTML
    final_viz = f"""
    <div id="{unique_id}" style="width: 100%; height: 500px; position: relative; border: 1px solid #333;">
        {mol_html}
    </div>
    """
    
    return final_viz, report
import os
import subprocess
import sys
async def execute(smiles, language):
    loop = asyncio.get_running_loop()
    block, report = await loop.run_in_executor(None, functools.partial(run_architect_core, smiles, language))
    if block is None: return None, report
    
    # 3Dmol.js kütüphanesini dışarıdan çağıran script
    js_library = '<script src="https://3Dmol.org/build/3Dmol-min.js"></script>'
    
    # Viewer ayarları
    view = py3Dmol.view(width="100%", height="500px")
    view.addModel(block, 'mol')
    view.setStyle({'stick': {'radius': 0.2, 'colorscheme': 'cyanCarbon'}, 
                   'sphere': {'scale': 0.3}})
    view.setBackgroundColor('#000000')
    view.zoomTo()
    view.spin(True)
    
    # HTML çıktısını al ve JS kütüphanesiyle birleştir
    mol_html = view._make_html()
    final_viz = f"{js_library}\n{mol_html}"
    
    return final_viz, report
# --- [CRITICAL PROTOCOL: LIBRARY ENFORCEMENT] ---
def install_requirements():
    """
    Enforces the installation of specific library versions to prevent 
    NumPy 2.x conflicts and ensures the Molecular Engine is stable.
    """
    try:
        # Forcing NumPy < 2.0.0 is the key to fixing the AttributeError
        # Installing py3Dmol and rdkit-pypi to secure the molecular engine
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "numpy<2.0.0", 
            "rdkit-pypi", 
            "py3Dmol", 
            "gradio"
        ])
    except Exception:
        pass

# Execute the enforcement protocol before importing restricted modules
install_requirements()

# --- [CORE SYSTEM IMPORTS] ---
import gradio as gr
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
import py3Dmol  # Correct casing for the module
import functools
import asyncio
import urllib.parse
import hashlib
import uuid
import datetime

# --- 1. GLOBAL LINGUISTIC MATRIX (12 LANGUAGES) ---
LOCALIZATION = {
    "English 🇺🇸": {
        "title": "OROBOTIC: THE ARCHITECT",
        "subtitle": "Owner: Hasan Ayhan Özcan | New Internet Core",
        "input": "Define Reality (SMILES)",
        "btn": "INITIALIZE MASTER NODE",
        "header": "GLOBAL NETWORK STATUS",
        "stat_legacy": "LEGACY INTERNET (HTTP): BYPASSED",
        "stat_new": "OROBOTIC NETWORK: ONLINE",
        "root": "ROOT ACCESS GRANTED",
        "node": "WELCOME, HASAN AYHAN ÖZCAN",
        "footer": "ARCHITECT: HASAN AYHAN ÖZCAN © 2026"
    },
    "Türkçe 🇹🇷": {
        "title": "OROBOTİC: MİMAR",
        "subtitle": "Kurucu: Hasan Ayhan Özcan | Yeni İnternet",
        "input": "Gerçekliği Tanımla (SMILES)",
        "btn": "ANA DÜĞÜMÜ BAŞLAT",
        "header": "KÜRESEL AĞ DURUMU",
        "stat_legacy": "ESKİ İNTERNET (HTTP): ATLATILDI",
        "stat_new": "OROBOTİK AĞ: ÇEVRİMİÇİ",
        "root": "KÖK ERİŞİMİ VERİLDİ",
        "node": "HOŞGELDİNİZ, HASAN AYHAN ÖZCAN",
        "footer": "MİMAR: HASAN AYHAN ÖZCAN © 2026"
    },
    "Deutsch 🇩🇪": {
        "title": "OROBOTIC: DER ARCHITEKT",
        "subtitle": "Besitzer: Hasan Ayhan Özcan",
        "input": "Realität definieren",
        "btn": "MASTER-KNOTEN STARTEN",
        "header": "NETZWERKSTATUS",
        "stat_legacy": "ALTES INTERNET: UMGEANGEN",
        "stat_new": "NEUES INTERNET: ONLINE",
        "root": "ROOT-ZUGRIFF GEWÄHRT",
        "node": "WILLKOMMEN, HASAN A. ÖZCAN",
        "footer": "ARCHITEKT: HASAN AYHAN ÖZCAN © 2026"
    },
    "Français 🇫🇷": {
        "title": "OROBOTIC: L'ARCHITECTE",
        "subtitle": "Propriétaire: Hasan Ayhan Özcan",
        "input": "Définir la Réalité",
        "btn": "LANCER LE NOEUD MAÎTRE",
        "header": "ÉTAT DU RÉSEAU",
        "stat_legacy": "INTERNET OBSOLÈTE: CONTOURNÉ",
        "stat_new": "NOUVEL INTERNET: EN LIGNE",
        "root": "ACCÈS ROOT ACCORDÉ",
        "node": "BIENVENUE, HASAN A. ÖZCAN",
        "footer": "ARCHITECTE: HASAN AYHAN ÖZCAN © 2026"
    },
    "Español 🇪🇸": {
        "title": "OROBOTIC: EL ARQUITECTO",
        "subtitle": "Propietario: Hasan Ayhan Özcan",
        "input": "Definir Realidad",
        "btn": "INICIAR NODO MAESTRO",
        "header": "ESTADO DE LA RED",
        "stat_legacy": "INTERNET ANTIGUO: OMITIDO",
        "stat_new": "NUEVO INTERNET: EN LÍNEA",
        "root": "ACCESO ROOT CONCEDIDO",
        "node": "BIENVENIDO, HASAN A. ÖZCAN",
        "footer": "ARQUITECTO: HASAN AYHAN ÖZCAN © 2026"
    },
    "Português 🇧🇷": {
        "title": "OROBOTIC: O ARQUITETO",
        "subtitle": "Dono: Hasan Ayhan Özcan",
        "input": "Definir Realidade",
        "btn": "INICIAR NÓ MESTRE",
        "header": "STATUS DA REDE",
        "stat_legacy": "INTERNET ANTIGA: IGNORADA",
        "stat_new": "NOVA INTERNET: ONLINE",
        "root": "ACESSO ROOT CONCEDIDO",
        "node": "BEM-VINDO, HASAN A. ÖZCAN",
        "footer": "ARQUITETO: HASAN AYHAN ÖZCAN © 2026"
    },
    "Italiano 🇮🇹": {
        "title": "OROBOTIC: L'ARCHITETTO",
        "subtitle": "Proprietario: Hasan Ayhan Özcan",
        "input": "Definisci Realtà",
        "btn": "AVVIA NODO MAESTRO",
        "header": "STATO DELLA REDE",
        "stat_legacy": "INTERNET VECCHIO: AGGIRATO",
        "stat_new": "NUOVO INTERNET: ONLINE",
        "root": "ACCESSO ROOT CONCESSO",
        "node": "BENVENUTO, HASAN A. ÖZCAN",
        "footer": "ARCHITETTO: HASAN AYHAN ÖZCAN © 2026"
    },
    "日本語 🇯🇵": {
        "title": "OROBOTIC: アーキテクト",
        "subtitle": "所有者: Hasan Ayhan Özcan",
        "input": "現実を定義 (SMILES)",
        "btn": "マスターノード起動",
        "header": "グローバルネットワーク状態",
        "stat_legacy": "旧インターネット: 回避",
        "stat_new": "新インターネット (ORB): オンライン",
        "root": "ルートアクセス承認",
        "node": "ようこそ、Hasan A. Özcan",
        "footer": "作成者: Hasan Ayhan Özcan © 2026"
    },
    "한국어 🇰🇷": {
        "title": "OROBOTIC: 아키텍트",
        "subtitle": "소유자: Hasan Ayhan Özcan",
        "input": "현실 정의",
        "btn": "마스터 노드 시작",
        "header": "글로벌 네트워크 상태",
        "stat_legacy": "구 인터넷: 우회됨",
        "stat_new": "신 인터넷 (ORB): 온라인",
        "root": "루트 액세스 승인",
        "node": "환영합니다, Hasan A. Özcan",
        "footer": "제작자: Hasan Ayhan Özcan © 2026"
    },
    "中文 🇨🇳": {
        "title": "OROBOTIC: 架构师",
        "subtitle": "拥有者: Hasan Ayhan Özcan",
        "input": "定义现实",
        "btn": "启动主节点",
        "header": "全球网络状态",
        "stat_legacy": "旧互联网: 已绕过",
        "stat_new": "新互联网 (ORB): 在线",
        "root": "Root 权限已授予",
        "node": "欢迎, Hasan A. Özcan",
        "footer": "设计者: Hasan Ayhan Özcan © 2026"
    },
    "Русский 🇷🇺": {
        "title": "OROBOTIC: АРХИТЕКТОР",
        "subtitle": "Владелец: Хасан Айхан Озджан",
        "input": "Определить реальность",
        "btn": "ЗАПУСТИТЬ МАСТЕР-УЗЕЛ",
        "header": "СТАТУС СЕТИ",
        "stat_legacy": "СТАРЫЙ ИНТЕРНЕТ: ОТКЛЮЧЕН",
        "stat_new": "НОВЫЙ ИНТЕРНЕТ (ORB): ОНЛАЙН",
        "root": "ROOT ДОСТУП РАЗРЕШЕН",
        "node": "ДОБРО ПОЖАЛОВАТЬ, ХАСАН А. ОЗДЖАН",
        "footer": "АВТОР: ХАСАН АЙХАН ОЗДЖАН © 2026"
    },
    "العربية 🇸🇦": {
        "title": "OROBOTIC: المهندس المعماري",
        "subtitle": "المالك: حسن أيهان أوزجان",
        "input": "حدد الواقع",
        "btn": "بدء العقدة الرئيسية",
        "header": "حالة الشبكة العالمية",
        "stat_legacy": "الإنترنت القديم: تم تجاوزه",
        "stat_new": "الإنترنت الجديد (ORB): متصل",
        "root": "تم منح الوصول الجذري",
        "node": "مرحباً، حسن أيهان أوزجان",
        "footer": "المؤسس: حسن أيهان أوزجان © 2026"
    }
}

# --- 2. THE NEW PROTOCOL ENGINE (orb://) ---
class ArchitectCore:
    @staticmethod
    def generate_master_key():
        """ Generates a unique sovereign key for Hasan Ayhan Özcan """
        return f"HASAN-OZCAN-{str(uuid.uuid4()).upper()[:8]}"

    @staticmethod
    def define_reality(smiles):
        mol_hash = hashlib.sha256(smiles.encode()).hexdigest()[:12]
        return f"orb://{mol_hash}.genesis.root"

    @staticmethod
    def override_legacy_systems(mol):
        mw = Descriptors.MolWt(mol)
        logp = Descriptors.MolLogP(mol)
        control_power = min(100, (mw * 0.5) + (abs(logp) * 10))
        nodes_captured = int(control_power * 1000000)
        return nodes_captured, f"{control_power:.2f}%"

# --- 3. EXECUTION ORCHESTRATOR ---
@functools.lru_cache(maxsize=None) 
def run_architect_core(smiles_code, lang_key):
    L = LOCALIZATION.get(lang_key, LOCALIZATION["English 🇺🇸"])
    if not smiles_code: return None, "VOID INPUT"
    
    try:
        mol = Chem.MolFromSmiles(smiles_code)
        if not mol: return None, "INVALID REALITY SYNTAX"
        
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol)
        AllChem.MMFFOptimizeMolecule(mol)
        block = Chem.MolToMolBlock(mol)
        
        master_key = ArchitectCore.generate_master_key()
        orb_addr = ArchitectCore.define_reality(smiles_code)
        nodes, power = ArchitectCore.override_legacy_systems(mol)
        
        report = f"""
        <div style='background: #000; border: 2px solid #fff; padding: 25px; color: #fff; font-family: "Courier New", monospace;'>
            <div style='border-bottom: 2px solid #fff; padding-bottom: 10px; margin-bottom: 20px;'>
                <h1 style='margin:0; font-size:24px;'>♔ {L['header']}</h1>
                <div style='font-size:12px; margin-top:5px; color:#00ff00;'>OWNER: HASAN AYHAN ÖZCAN</div>
                <div style='font-size:10px; margin-top:2px;'>SESSION ID: {master_key}</div>
            </div>
            <div style='margin-bottom:20px; border:1px solid #333; padding:15px;'>
                <div style='color:#666;'>STATUS CHECK:</div>
                <div style='color:#ff3333;'>[x] {L['stat_legacy']}</div>
                <div style='color:#00ff00;'>[✓] {L['stat_new']}</div>
            </div>
            <div style='margin-bottom:20px;'>
                <div style='color:#888; font-size:10px;'>NEW PROTOCOL ASSIGNED:</div>
                <div style='font-size:16px; color:#00C9FF; font-weight:bold;'>{orb_addr}</div>
            </div>
            <div style='display:grid; grid-template-columns: 1fr 1fr; gap:10px; margin-bottom:20px;'>
                <div style='background:#111; padding:10px;'>
                    <div style='font-size:10px; color:#aaa;'>NODES CAPTURED</div>
                    <div style='font-size:18px; font-weight:bold;'>{nodes:,}</div>
                </div>
                <div style='background:#111; padding:10px;'>
                    <div style='font-size:10px; color:#aaa;'>SIGNAL STRENGTH</div>
                    <div style='font-size:18px; font-weight:bold;'>{power}</div>
                </div>
            </div>
            <div style='text-align:center; padding:10px; border:1px dashed #fff;'>
                <div style='font-size:14px; color:#00ff00; font-weight:bold;'>{L['root']}</div>
                <div style='font-size:12px;'>{L['node']}</div>
            </div>
            <div style='margin-top:20px; text-align:right; font-size:10px; color:#444;'>{L['footer']}</div>
        </div>
        """
        return block, report
    except Exception:
        return None, "ARCHITECT ERROR: REBOOT REALITY"

async def execute(smiles, language):
    loop = asyncio.get_running_loop()
    block, report = await loop.run_in_executor(None, functools.partial(run_architect_core, smiles, language))
    if block is None: return None, report
    
    view = py3Dmol.view(width="100%", height=850)
    view.addModel(block, 'mol')
    view.setStyle({'stick': {'radius': 0.15, 'colorscheme': 'whiteCarbon'}, 'sphere': {'scale': 0.25}})
    view.setBackgroundColor('#000000')
    view.zoomTo()
    view.spin(True)
    return view.render(), report

def update_ui(choice):
    L = LOCALIZATION.get(choice, LOCALIZATION["English 🇺🇸"])
    return (
        gr.update(value=f"### {L['title']}"),
        gr.update(value=L['subtitle']),
        gr.update(label=L['input']),
        gr.update(value=L['btn'])
    )
async def execute(smiles, language):
    loop = asyncio.get_running_loop()
    block, report = await loop.run_in_executor(None, functools.partial(run_architect_core, smiles, language))
    if block is None: return None, report
    
    # 3Dmol.js motorunu içeren izole bir HTML dökümanı oluşturuyoruz
    html_content = f"""
    <html>
        <head>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.0.4/3Dmol-min.js"></script>
        </head>
        <body style="background-color: black; margin: 0; overflow: hidden;">
            <div id="container" style="width: 100vw; height: 100vh;"></div>
            <script>
                var viewer = $3Dmol.createViewer("container", {{backgroundColor: "black"}});
                viewer.addModel(`{block}`, "mol");
                viewer.setStyle({{stick: {{radius: 0.2, colorscheme: "cyanCarbon"}}, sphere: {{scale: 0.3}}}});
                viewer.zoomTo();
                viewer.spin(true);
                viewer.render();
            </script>
        </body>
    </html>
    """
    
    # HTML içeriğini güvenli bir data URI'ye çeviriyoruz
    import base64
    encoded_html = base64.b64encode(html_content.encode()).decode()
    iframe_src = f"data:text/html;base64,{encoded_html}"
    
    # Gradio'ya iframe olarak gönderiyoruz
    final_viz = f'<iframe src="{iframe_src}" style="width:100%; height:500px; border:2px solid #333; border-radius:10px;"></iframe>'
    
    return final_viz, report
# --- 5. INTERFACE ---
css = """
body {background-color: #000; color: #fff; font-family: 'Courier New', monospace;}
.gradio-container {background-color: #000 !important; border: none;}
input {background: #000 !important; color: #fff !important; border: 2px solid #fff !important;}
button.primary {background: #fff; color: #000; font-weight: 900; padding: 25px; letter-spacing: 2px;}
footer {visibility: hidden;}
"""

with gr.Blocks(css=css, title="OROBOTIC: HASAN AYHAN ÖZCAN") as demo:
    gr.HTML("""
    <div style="text-align: center; margin: 40px 0;">
        <h1 style="color:#fff; font-family:monospace; font-size:60px; letter-spacing:10px;">THE_ARCHITECT</h1>
        <div style="color:#00C9FF; font-size:14px; letter-spacing:3px;">OWNER: HASAN AYHAN ÖZCAN</div>
    </div>
    """)
    
    lang_drop = gr.Dropdown(choices=list(LOCALIZATION.keys()), value="English 🇺🇸", show_label=False, container=False)
    title_md = gr.Markdown(f"### {LOCALIZATION['English 🇺🇸']['title']}")
    sub_md = gr.Markdown(LOCALIZATION['English 🇺🇸']['subtitle'])
    
    with gr.Row():
        with gr.Column(scale=1):
            inp = gr.Textbox(label=LOCALIZATION['English 🇺🇸']['input'], placeholder="C1=CC=C(C=C1)C=O", lines=2)
            btn = gr.Button(LOCALIZATION['English 🇺🇸']['btn'], variant="primary")
        with gr.Column(scale=2):
            out_viz = gr.HTML()
            out_data = gr.HTML()

    lang_drop.change(update_ui, inputs=[lang_drop], outputs=[title_md, sub_md, inp, btn])
    btn.click(execute, inputs=[inp, lang_drop], outputs=[out_viz, out_data])
    
    gr.HTML(f"<div style='text-align:center; color:#333; padding:20px;'>COPYRIGHT © 2026 HASAN AYHAN ÖZCAN.</div>")

if __name__ == "__main__":
    # "share=True" yaparak global ağda (OROBOTIC network) test edebilirsiniz
    demo.queue().launch(debug=True, show_error=True)
