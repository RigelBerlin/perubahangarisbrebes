import streamlit as st
import numpy as np
import folium
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu
import geopandas as gd
import pandas as pd
import branca.colormap as cm
import plotly.express as px
from branca.colormap import StepColormap

st.set_page_config(layout="wide", page_title="Dashboard Prediksi Garis Pantai Kabupaten Brebes")

#####
st.markdown("""
    <style>
    /* Hilangkan padding bawaan dari main block */
    .block-container {
        padding-top: 0.5rem; /* default sekitar 6rem, ini kita kecilkan */
        padding-bottom: 0.5rem;
    }
    /* Ubah background seluruh halaman */
    .stApp {
        background-color: white;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)
#####

st.markdown("""
            <style>
            [data-testid="stSidebar"]{
                background-color: white;
                height: 100vh;
                display: flex;
                flex-direction: column;
            }
            [data-testid="stSidebar"] > div:first-child {
                background-color: white;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                flex: 1;
                border-right: 2px solid #ddd;
            }
            .sidebar-content{
                flex: 1;
                pdding: 1rem;
                overflow-y: auto;
            }
            .sidebar-footer{
                padding: 10px;
                font-size: 12px;
                text-align: center;
                border-top: 1px solid #ddd;
                margin-bottom: 10px;
                margin-top: 40vh;
                color: gray;
                font-weight: bold;
            }
            /* Header judul sidebar */
            .nav-header {
                color: #7a7a7a !important;
                font-weight: bold !important;
                text-align: center !important;
                align-items: center;
                padding-left: 10px !important; /* Tambah jarak dari kiri */
                font-size: 30px !important;
            }

            .card {
                background-color: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
                text-align: center;
                margin: 10px;
            }
            .card-title {
                font-size: 18px;
                font-weight: bold;
                color: #333333;
            }
            .card-value {
                font-size: 16px;
                color: #007acc;
                margin-top: 5px;
            }

            .card img {
                width: 60px;
                height: 60px;
                margin-right: 12px;
            }

            .card text {
                display: flex;
                flex-direction: column;
            }

            <div class="sidebar-footer">&copy; 2025</div>
            </style>
    """, unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("""<div class='nav-header'><img src='https://cdn-icons-png.flaticon.com/512/4336/4336883.png' 
                    alt='icon' 
                    style='width:30px; height:30px; vertical-align:middle; margin-right:15px;'>
                        Garis Pantai Brebes
                    </div>
                """, unsafe_allow_html=True)
    menu = option_menu(
        "x",
        [   
            "Home",
            "Informasi Garis Pantai",
            "Analisis Perubahan Garis Pantai",
            "Prediksi Garis Pantai",
        ],
            icons=['info-circle', 'map', 'graph-up', 'water', 'check-circle'],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {
                    "padding": "5px", 
                    "background-color": "#ffffff",  # putih
                },
                "icon": {
                    "color": "#7a7a7a",
                    "font-size": "18px"
                },
                "nav-link": {
                    "font-size": "16px", 
                    "text-align": "left", 
                    "margin": "0px",
                    "--hover-color": "#f2f2f2",  # biru muda saat hover
                    "color": "#7a7a7a",  # teks biru
                    "font-weight": "bold"
                },
                "nav-link-selected": {
                    "background-color": "#e6e6e6",  # biru tua saat aktif
                    "color": "#7a7a7a"
                }
            }
    )

    st.markdown('<div class="sidebar-footer">© 2025 Dashboard Prediksi Garis Pantai</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if menu == "Home":
    st.title("Prediksi Perubahan Garis Pantai")
    ##################################
    # Layout card
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
            <div class="card">
                <img src='https://cdn-icons-png.flaticon.com/512/4336/4336883.png' alt='icon'>
                <div class="card-text">
                    <div class="card-title">Garis Pantai 2024</div>
                    <div class="card-value">76.024,26 meter</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="card">
                <img src='https://cdn-icons-png.flaticon.com/512/6012/6012178.png' alt='icon'>
                <div class="card-text">
                    <div class="card-title">Lokus Penelitian</div>
                    <div class="card-value">Kabupaten Brebes</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="card">
                <img src='https://cdn-icons-png.flaticon.com/512/477/477483.png' alt='icon'>
                <div class="card-text">
                    <div class="card-title">Jumlah Garis Pantai</div>
                    <div class="card-value">8 (1990-2024)</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <div class="card">
                <img src='https://cdn-icons-png.flaticon.com/512/2784/2784459.png' alt='icon'>
                <div class="card-text">
                    <div class="card-title">Periode Prediksi</div>
                    <div class="card-value">2034 dan 2044</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    ##################################

    # === 1. Baca data dari shapefile ===
    shp_path = "D:/Skripsi_shoreline change/GarisPantai19902024.shp"
    gdf = gd.read_file(shp_path)

    # Pastikan DATE_ sebagai datetime
    gdf["DATE_"] = pd.to_datetime(gdf["DATE_"], errors="coerce")
    gdf["tahun"] = gdf["DATE_"].dt.year

    # Agregasi per tahun
    data = (
        gdf.groupby("tahun")
        .agg({
            "SHAPE_Leng": "sum",
            "UNCERTAINT": "mean"
        })
        .reset_index()
        .rename(columns={
            "SHAPE_Leng": "Panjang Garis Pantai",
            "UNCERTAINT": "Uncertainty"
        })
    )

    # === 2. Styling Card ===
    st.markdown("""
    <style>
    .smooth-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Grafik batang descending Panjang Garis Pantai
    df_sorted_length = data.sort_values(by="Panjang Garis Pantai", ascending=True)
    fig_bar_length = px.bar(df_sorted_length,
                            x="tahun", y="Panjang Garis Pantai",
                            title="Panjang Garis Pantai",
                            labels={"tahun": "Tahun", "Panjang Garis Pantai": "Panjang (m)"},
                            text_auto=".2s")
    fig_bar_length.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="black"),
        title_font=dict(color="black", size=16),
        margin=dict(l=20, r=20, t=40, b=20),
        shapes=[
            dict(
                type="rect",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                line=dict(color="black", width=2),
                fillcolor="rgba(0,0,0,0)"
            )
        ],
        xaxis=dict(
            title_font=dict(color="black", size=14),
            tickfont=dict(color="black")
        ),
        yaxis=dict(
            title_font=dict(color="black", size=14),
            tickfont=dict(color="black")
        )
    )

    # Grafik garis Panjang Garis Pantai per tahun
    fig_line = px.line(data,
                    x="tahun", y="Panjang Garis Pantai",
                    title="Panjang Garis Pantai per Tahun",
                    markers=True,
                    labels={"tahun": "Tahun", "Panjang Garis Pantai": "Panjang (m)"})
    fig_line.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="black"),
        title_font=dict(color="black", size=16),
        margin=dict(l=20, r=20, t=40, b=20),
        shapes=[
            dict(
                type="rect",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                line=dict(color="black", width=2),
                fillcolor="rgba(0,0,0,0)"
            )
        ],
        xaxis=dict(
            title_font=dict(color="black", size=14),
            tickfont=dict(color="black")
        ),
        yaxis=dict(
            title_font=dict(color="black", size=14),
            tickfont=dict(color="black")
        )
    )
    max_length = df_sorted_length["Panjang Garis Pantai"].max()
    fig_line.update_yaxes(range=[0,max_length*1.05])
    
    # Grafik batang descending Uncertainty
    df_sorted_unc = data.sort_values(by="Uncertainty", ascending=False)
    fig_bar_unc = px.bar(df_sorted_unc,
                        x="tahun", y="Uncertainty",
                        title="Uncertainty Garis Pantai",
                        labels={"tahun": "Tahun", "Uncertainty": "Nilai"},
                        text_auto=".2f")
    fig_bar_unc.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="black"),
        title_font=dict(color="black", size=16),
        margin=dict(l=20, r=20, t=40, b=20),
        shapes=[
            dict(
                type="rect",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                line=dict(color="black", width=2),
                fillcolor="rgba(0,0,0,0)"
            )
        ],
        xaxis=dict(
            title_font=dict(color="black", size=14),
            tickfont=dict(color="black")
        ),
        yaxis=dict(
            title_font=dict(color="black", size=14),
            tickfont=dict(color="black")
        )
    )

    # === 4. Tampilkan di dalam card ===
    with st.container():
        col_left, col_right= st.columns([2,2])
        with col_left:
            fig_bar_length.update_layout(height=250)
            st.plotly_chart(fig_bar_length, use_container_width=True)
            fig_line.update_layout(height=250)
            st.plotly_chart(fig_line, use_container_width=True)
        with col_right:
            fig_bar_unc.update_layout(height=510)
            st.plotly_chart(fig_bar_unc, use_container_width=True)

    ########################################
    st.markdown("""
                <div style="
                    max-width: 900px;
                    margin: 30px auto;
                    font-size: 16px;
                    line-height: 1.7;
                    text-align: justify;
                    color: #333;
                ">
                Dashboard ini dikembangkan untuk menampilkan hasil deteksi dan prediksi perubahan garis pantai di Kabupaten Brebes secara interaktif.
                Data yang digunakan berasal dari hasil analisis citra satelit dan prediksi menggunakan metode Kalman Filtering. Kabupaten Brebes, sebuah 
                kabupaten di Jawa Tengah yang diketahui mengalami perubahan garis pantai yang cukup signifikan akibat faktor alami maupun aktivitas manusia, 
                fenomena terjadinya perubahan garis pantai ini mendorong untuk perlunya identifikasi terhadap dinamika perubahan garis pantai yang terjadi. Untuk mencapai tujuan tersebut, dilakukan identifikasi perubahan garis pantai yaitu metode machine learning dan metode indeks. 
                </div>
                """, unsafe_allow_html=True)
elif menu == "Informasi Garis Pantai":
    st.markdown("""
        <style>
        /* Cari elemen label yang mengandung teks tertentu */
        .stMultiSelect label p {
            color: green !important;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)
    st.title ("Informasi Garis Pantai")
    st.caption("Deteksi Garis Pantai Tahun 1990-2024")
    shp_path = "shapefile/GarisPantai19902024.shp"

    # Load SHP
    try:
        gdf = gd.read_file(shp_path).to_crs(epsg=4326)
    except Exception as e:
        st.error(f"Gagal memuat SHP: {e}")
        st.stop()

    # Pastikan kolom DATE_ menjadi datetime
    gdf["DATE_"] = pd.to_datetime(gdf["DATE_"], errors="coerce")
    gdf["tahun"] = gdf["DATE_"].dt.year

    # Pilihan tahun yang tersedia
    tahun_opsi = [1990, 1995, 2000, 2005, 2010, 2015, 2020, 2024]
    tahun_dipilih = st.multiselect("📅 Pilih Tahun Garis Pantai", tahun_opsi, default=[2024])

    if not tahun_dipilih:
        st.warning("Silakan pilih minimal satu tahun.")
        st.stop()

    # Filter berdasarkan tahun dipilih
    gdf_selected = gdf[gdf["tahun"].isin(tahun_dipilih)]

    if gdf_selected.empty:
        st.warning("Tidak ada data untuk tahun yang dipilih.")
        st.stop()

    # Peta warna formal
    colors = {
        1990: "#1f77b4",  # Biru
        1995: "#ff7f0e",  # Oranye
        2000: "#2ca02c",  # Hijau
        2005: "#d62728",  # Merah
        2010: "#9467bd",  # Ungu
        2015: "#8c564b",  # Cokelat
        2020: "#e377c2",  # Pink
        2024: "#7f7f7f"   # Abu-abu
    }

    # Tentukan pusat peta
    center = gdf_selected.unary_union.centroid
    m = folium.Map(location=[center.y, center.x], zoom_start=13, control_scale=True)

    # Tambahkan Google Maps layer
    folium.TileLayer(
        tiles='http://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}',
        attr='Google Maps',
        name='Google Maps',
        overlay=False,
        control=True
    ).add_to(m)

    # Tambahkan garis pantai sesuai tahun
    for year in sorted(tahun_dipilih):
        gdf_year = gdf_selected[gdf_selected["tahun"] == year].drop(columns=["DATE_"])
        folium.GeoJson(
            gdf_year,
            name=f"Garis Pantai {year}",
            style_function=lambda feature, warna=colors[year]: {
                "color": warna,
                "weight": 3
            },
            tooltip=folium.GeoJsonTooltip(
                fields=["tahun", "SHAPE_Leng", "UNCERTAINT"],
                aliases=["Tahun:", "Panjang (m):", "Uncertainty:"],
                localize=True
            )
        ).add_to(m)

    # Tampilkan peta
    st.subheader("🗺️ Peta Garis Pantai")
    st_folium(m, width=None, height=600)

    # Tampilkan tabel data
    st.subheader("📋 Data Garis Pantai")
    st.dataframe(gdf_selected[["tahun", "SHAPE_Leng", "UNCERTAINT"]])

elif menu == "Analisis Perubahan Garis Pantai":
    st.title("📊 Analisis Perubahan Garis Pantai per Transek")
    st.caption("Menampilkan nilai statistik per transek dengan warna gradasi sesuai metodenya.")

    shp_path_statistik = "shapefile/AnalisisPerubahan.shp"

    try:
        gdf_stat = gd.read_file(shp_path_statistik).to_crs(epsg=4326)
    except Exception as e:
        st.error(f"Gagal memuat SHP statistik: {e}")
        st.stop()

    # Pilihan metode statistik
    metode_list = ["SCE", "NSM", "EPR", "LRR", "WLR"]
    metode_dipilih = st.selectbox("Pilih Metode Statistik", metode_list)

    # Ambil nilai kolom yang dipilih
    nilai = gdf_stat[metode_dipilih]

    min_val = nilai.min()
    max_val = nilai.max()
    mean_val = nilai.mean()
    std_val = nilai.std()

    # Fungsi untuk breaks berdasarkan standar deviasi
    def create_breaks_stdev(data, num_classes=7):
        mean_val = np.mean(data)
        std_val = np.std(data)
        breaks = [mean_val + (i - num_classes // 2) * std_val for i in range(num_classes + 1)]
        breaks = sorted(breaks)
        breaks[0] = np.min(data)
        breaks[-1] = np.max(data)
        return breaks

    # Fungsi colormap
    def create_dsas_colormap(data, metode):
        colors = [
            '#a50f15',
            '#de2d26',
            '#fb6a4a',
            '#fcae91',
            '#f0f0f0',
            '#bdd7e7',
            '#6baed6',
            '#3182bd',
            '#08519c'
        ]

        if metode in ['SCE', 'NSM']:
            breaks = create_breaks_stdev(data)
        elif metode in ['EPR', 'LRR', 'WLR']:
            # Breaks tetap (ArcMap style)
            fixed_bins = [-3.0, -2.0, -1.0, -0.5, 0.5, 1.0, 2.0, 3.0]
            # Tambahkan min dan max dari data ke ujung breaks
            breaks = [min_val] + fixed_bins + [max_val]
        else:
            raise ValueError("Metode tidak dikenali")

        colormap = StepColormap(
            colors=colors,
            index=breaks,
            vmin=min_val,
            vmax=max_val,
            caption=f'Colormap DSAS metode {metode}'
        )
        return colormap, breaks

    colormap, breaks = create_dsas_colormap(nilai, metode_dipilih)
    
    # Tentukan pusat peta
    center = gdf_stat.unary_union.centroid
    m = folium.Map(location=[center.y, center.x], zoom_start=13, control_scale=True)

    # Layer Google Maps
    folium.TileLayer(
        tiles='http://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}',
        attr='Google Maps',
        name='Google Maps',
        overlay=False,
        control=True
    ).add_to(m)

    # Tambahkan transek ke peta dengan warna sesuai nilai metode
    def status_perubahan(val):
        if val < 0:
            return "Abrasi"
        elif val > 0:
            return "Akresi"
        else:
            return "Stabil"
    if metode_dipilih != "SCE":
        gdf_stat["Status"] = gdf_stat[metode_dipilih].apply(status_perubahan)

    # Konfigurasi tooltip per metode
    if metode_dipilih == "SCE":
        tooltip_fields = ["TransectID", "SCE"]
        tooltip_aliases = ["Transect ID: ", "SCE: "]
    else:
        tooltip_fields = ["TransectID", "Status", metode_dipilih]
        tooltip_aliases = ["Transect ID: ", "Status: ", f"{metode_dipilih}: "]

    # Tambahkan layer GeoJson
    folium.GeoJson(
        gdf_stat,
        name=f"Transek - {metode_dipilih}",
        style_function=lambda feature: {
            "color": colormap(feature["properties"][metode_dipilih]),
            "weight": 3
        },
        tooltip=folium.GeoJsonTooltip(
            fields=tooltip_fields,
            aliases=tooltip_aliases,
            localize=True,
            labels=True,
            sticky=True
        )
    ).add_to(m)

    colormap.caption = f"{metode_dipilih}"
    colormap.add_to(m)

    # Tampilkan peta
    st.subheader(f"🗺️ Peta Transek Berdasarkan {metode_dipilih}")
    st_folium(m, width=None, height=600)
elif menu == "Prediksi Garis Pantai":
    st.markdown("""
    <style>
        * {
            color: black !important;
        }
        
        .stMarkdown, .stSubheader, .stCaption, .stText, .stDataFrame, .css-10trblm, .css-1d391kg {
            color: black !important;
        }

        .stDataFrame div {
            color: black !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("🌊 Garis Pantai di Kabupaten Brebes")
    st.caption("Hasil Prediksi Garis Pantai tahun 2034 dan 2044 berdasarkan Kalman Filtering")
    shp_path_2034 = "shapefile/Garis_Pantai_2034.shp" #Impor Shapefile 2034
    shp_path_2044 = "shapefile/Garis_Pantai_2044.shp" #Impor Shapefile 2044
    try:
        gdf_2034 = gd.read_file(shp_path_2034).to_crs(epsg=4326)
        gdf_2034["year"]=2034
        gdf_2044 = gd.read_file(shp_path_2044).to_crs(epsg=4326)
        gdf_2044["year"]=2044
    except Exception as e:
        st.error(f"Gagal memuat SHP: {e}")
        st.stop()

    #PILIH TAHUN PREDIKSI

    st.subheader("📅 Pilih Tahun Prediksi yang Ingin Ditampilkan")
    col1, col2 = st.columns(2)

    with col1:
        show_2034 = st.checkbox("Tampilkan Tahun 2034", value=False)
    with col2:
        show_2044 = st.checkbox("Tampilkan Tahun 2044", value=False)

    # Kumpulkan tahun yang dipilih
    tahun_dipilih = []
    if show_2034:
        tahun_dipilih.append(2034)
    if show_2044:
        tahun_dipilih.append(2044)

    if not tahun_dipilih:
        st.warning("Silakan centang minimal satu tahun untuk ditampilkan.")
        st.stop()

    # Filter data berdasarkan tahun yang dipilih
    gdf_all = gd.GeoDataFrame(pd.concat([gdf_2034, gdf_2044], ignore_index=True), crs="EPSG:4326")
    gdf_selected = gdf_all[gdf_all['year'].isin(tahun_dipilih)]

    # ----------------------------
    # TAMPILKAN PETA FOLIUM
    # ----------------------------
    if gdf_selected.empty:
        st.warning("Tidak ada data untuk tahun yang dipilih.")
        st.stop()

    colors={
        10: "blue",
        20: "yellow"
    }

    center = gdf_selected.unary_union.centroid
    m = folium.Map(location=[center.y, center.x], zoom_start=13, control_scale=True)


    # Tambahkan layer Google Maps
    folium.TileLayer(
        tiles='http://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}',
        attr='Google Maps',
        name='Google Maps',
        overlay=False,
        control=True
    ).add_to(m)

    # Tambahkan garis ke peta
    folium.GeoJson(
        gdf_selected,
        name="Garis Prediksi",
        style_function=lambda feature: {
            "color": colors.get(round(float(feature["properties"].get("ForecastPe")),1), "blue"),
            "weight": 3
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["ForecastYe", "ForecastPe", "SHAPE_Leng"],
            aliases=["Tahun Prediksi: ", "Periode Prediksi: ", "Panjang (m): "],
            localize=True
        )
    ).add_to(m)     

    # Tampilkan peta di Streamlit
    st.subheader("🗺️ Peta Titik Prediksi")
    st_folium(m, width=None, height=600)

elif menu == "Evaluasi Prediksi":
    st.title("🔄 Perbandingan Perubahan Garis Pantai")
    st.markdown("""
    Perbandingan dilakukan antar hasil prediksi tahun 2034 dan 2044 dengan garis pantai historis untuk melihat tren abrasi atau akresi.
    """)


