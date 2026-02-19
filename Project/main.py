import streamlit as st

# -----------------------------
# Page settings + background
# -----------------------------
st.set_page_config(page_title="Kelime Sözlüğü", page_icon="📚", layout="centered")

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
  background-color: #A547DE;
  opacity: 0.96;
  background-image:
    linear-gradient(135deg, #a547de 25%, transparent 25%),
    linear-gradient(225deg, #a547de 25%, transparent 25%),
    linear-gradient(45deg,  #a547de 25%, transparent 25%),
    linear-gradient(315deg, #a547de 25%, #A547DE 25%);
  background-position: 10px 0, 10px 0, 0 0, 0 0;
  background-size: 20px 20px;
  background-repeat: repeat;
}
.block-container { padding-top: 1.2rem; max-width: 860px; }
.card {
  background: rgba(255,255,255,0.88);
  border-radius: 18px;
  padding: 16px 16px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.10);
  border: 1px solid rgba(255,255,255,0.45);
}
.muted { color: rgba(15, 23, 42, 0.75); }
.small { font-size: 0.95rem; }
.badge {
  display:inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(165,71,222,0.18);
  color: #4b0082;
  font-weight: 600;
  font-size: 0.85rem;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# -----------------------------
# Data (kolay genişler)
# -----------------------------
WORDS = [
    {
        "kelime": "Başarı",
        "kategori": "Motivasyon",
        "emoji": "🏆",
        "tanim": "Başarı, bir işi istenilen bir biçimde tamamlamak ve hedeflenen sonuca ulaşmaktır."
    },
    {
        "kelime": "Özgüven",
        "kategori": "Psikoloji",
        "emoji": "🧠",
        "tanim": "Özgüven, kişinin kendi değerine ve becerilerine dair algısıdır. Düşünceleri, duyguları ve davranışları birlikte etkiler."
    },
    {
        "kelime": "Stres",
        "kategori": "Psikoloji",
        "emoji": "⚡",
        "tanim": "Stres; tehdit, baskı veya mücadele gerektiren durumlarda ortaya çıkan; bedensel ve zihinsel tepkileri tetikleyen bir durumdur."
    },
    {
        "kelime": "Gelecek",
        "kategori": "Zaman",
        "emoji": "🔮",
        "tanim": "Gelecek, henüz yaşanmamış olan zaman dilimidir. Felsefe, din ve bilimin temel konuları arasında yer alır."
    }
]

ALL_CATEGORIES = ["Hepsi"] + sorted({w["kategori"] for w in WORDS})

def filter_words(query: str, category: str):
    q = (query or "").strip().lower()
    out = []
    for w in WORDS:
        if category != "Hepsi" and w["kategori"] != category:
            continue
        hay = (w["kelime"] + " " + w["tanim"] + " " + w["kategori"]).lower()
        if q and q not in hay:
            continue
        out.append(w)
    return out

# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
    <div class="card">
      <div style="display:flex; align-items:center; justify-content:space-between; gap:12px;">
        <div>
          <div style="font-size: 1.6rem; font-weight: 800;">📚 Mini Kelime Sözlüğü</div>
          <div class="muted small">Kelime seç, ara, açıklamasını tek kartta gör. İstersen metni kopyala.</div>
        </div>
        <div class="badge">Streamlit</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# -----------------------------
# Controls
# -----------------------------
with st.container():
    c1, c2 = st.columns([2, 1])
    with c1:
        query = st.text_input("Arama", placeholder="Örn: başarı, stres, psikoloji…")
    with c2:
        category = st.selectbox("Kategori", ALL_CATEGORIES)

results = filter_words(query, category)

st.write("")

# -----------------------------
# Results list + selection
# -----------------------------
if not results:
    st.warning("Sonuç bulunamadı. Arama kelimesini değiştir veya kategoriyi 'Hepsi' yap.")
    st.stop()

labels = [f"{w['emoji']} {w['kelime']}  •  {w['kategori']}" for w in results]
selected_label = st.selectbox("Bir kelime seç", labels)

selected = results[labels.index(selected_label)]

# -----------------------------
# Detail card
# -----------------------------
st.markdown(
    f"""
    <div class="card">
      <div style="display:flex; align-items:center; gap:10px;">
        <div style="font-size: 2rem;">{selected['emoji']}</div>
        <div>
          <div style="font-size: 1.3rem; font-weight: 800;">{selected['kelime']}</div>
          <div class="muted small">Kategori: <b>{selected['kategori']}</b></div>
        </div>
      </div>
      <hr style="border:none; border-top:1px solid rgba(15,23,42,0.12); margin:12px 0;">
      <div style="font-size: 1.05rem; line-height: 1.55;">
        {selected['tanim']}
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# -----------------------------
# Copy + extras
# -----------------------------
copy_text = f"{selected['kelime']} — {selected['tanim']}"
st.text_area("Kopyalamak için", value=copy_text, height=90)

with st.expander("Kelime havuzunu genişletmek"):
    st.markdown(
        """
- `WORDS` listesinin içine yeni kayıt ekleyebilirsin.
- Her kayıt şu alanları içeriyor: `kelime`, `kategori`, `emoji`, `tanim`.
- Arama ve kategori filtreleri otomatik çalışır.
        """
    )
