# Import library yang dibutuhkan
import streamlit as st
import pandas as pd
import altair as alt

# Setup tampilan dashboard
st.set_page_config(
    page_title = 'Analisa Potensi Essential Oil Indonesia'
    ,layout='wide'
)

st.markdown("""
    <div style="text-align: center;">
        <h1>Analisa Potensi Essential Oil Indonesia</h1>
    </div>
    """, unsafe_allow_html=True)
# st.markdown("_italic_")
# st.markdown("__bold__")
# st.markdown("""
#     1. Number 1
#     2. Number 2
#     3. Number 3
# """)

tab1, tab2 = st.tabs(["Essential Oil EXIM", "Patchouli and Parfume"])
with tab1:
    st.header("Essential Oil EXIM")
    # Image
    from PIL import Image
    image = Image.open("patchouli.jpg")
    aspect_ratio = image.height / image.width

   
    new_width = 600
    new_height = int(new_width * aspect_ratio)
    resized_image = image.resize((new_width, new_height))

    col1, col2, col3 = st.columns([1,1,1])

    with col2:
        st.image(resized_image)

    st.markdown("""Essential Oil (Minyak Atsiri) telah digunakan selama ribuan tahun untuk berbagai tujuan, khususnya pengobatan dan wewangian. 
                Essential Oil merupakan cairan pekat yang mengandung senyawa aroma yang khas dari tumbuhan. Sebagai negara yang kaya akan jenis tumbuhan, 
                Indonesia merupakan tempat alami bagi berkembangnya industri ini. Terdapat sekitar 40 jenis yang diproduksi Indonesia, 12 diantaranya dikembangkan secara komersial dalam skala industri. 
                Minyak atsiri biasanya merupakan komoditas yang bernilai tinggi dan bervolume rendah. Ekspor minyak atsiri Indonesia melebihi US$ 124 juta pada 2010 dan industri parfume merupakan salah satu konsumen minyak atsiri terbesar. 
                Namun di Indonesia sendiri perkembangan produksi, ekspor maupun pemanfaatannya cenderung rendah dibandingkan potensi yang dimiliki, lalu faktor dan kemungkinan apa yang bisa dilakukan untuk memperbaiki ini?""")

    df = pd.read_csv('./capstone_project_farhan_sn/export_all.csv')
    # Membuat barchart
    st.header('Negara Pengekspor Essential Oil')

    # Menampilkan chart di Streamlit
    col1, col2 = st.columns(2)  

    # Mengurutkan data berdasarkan 'value_exported_2022_usd' secara descending
    df_sorted = df.sort_values('value_exported_2022_usd', ascending=False).head(11)

    # Membuat Bar Chart vertikal dengan urutan berdasarkan 'value_exported_2022_usd' terbesar
    bar_chart1 = alt.Chart(df_sorted).mark_bar().encode(
        y=alt.Y('value_exported_2022_usd:Q', title='Value Exported 2022 (USD)', sort='-x'),
        x=alt.X('country:N', sort=alt.EncodingSortField(field='value_exported_2022', order='ascending'), axis=alt.Axis(title='Country')),
        color=alt.condition(
            alt.datum.country == 'Indonesia',  
            alt.value('#FF6347'),  
            alt.value('#1E90FF')  
        )
    ).properties(
        width=600,
        height=400,
        title='Top 11 Countries by Exported Value in 2022'
    )

    # Filter untuk hanya mendapatkan data dengan 'trade_balance_2022_usd' yang minus
    df_minus = df[df['trade_balance_2022_usd'] < 0]

    # Mengurutkan data berdasarkan 'trade_balance_2022_usd' dari yang minus terbesar ke terkecil
    df_minus_sorted = df_minus.sort_values('trade_balance_2022_usd', ascending=True).head(11)

    # Membuat Bar Chart dengan urutan negara yang eksplisit
    country_order = df_minus_sorted['country'].tolist()

    # Membuat bar chart
    bar_chart2 = alt.Chart(df_minus_sorted).mark_bar().encode(
        y=alt.Y('country:N', 
                sort=country_order,  
                axis=alt.Axis(title='Country')),
        x=alt.X('trade_balance_2022_usd:Q', title='Trade Balance 2022 (USD)'),
        color=alt.condition(
            alt.datum.country == 'Indonesia',  
            alt.value('#FF6347'),  
            alt.value('#1E90FF')  
        )
    ).properties(
        width=600,
        height=400,
        title='Countries with Negative Trade Balance in 2022'
    )

    col1, spacer, col2 = st.columns([1, 0.1, 1])  

    with col1:
        st.altair_chart(bar_chart1, use_container_width=True)  

    with spacer:
        st.write("")  

    with col2:
        st.altair_chart(bar_chart2, use_container_width=True)

    # Penjelasan barchart 1 dan 2
    st.markdown("""Berdasarkan data dari (https://www.trademap.org/Index.aspx) Indonesia masuk sebagai 10 besar negara peng ekspor Essential Oil (HS 3301) tahun 2022. 
                Namun sayangnya _trade balance_ dari Indonesia juga masih menunjukkan angka minus. Ini berarti Indonesia masih mengalami defisit dalam hal value export untuk komoditi ini.
                Namun kabar baiknya berdasarkan data tersebut Indonesia mempunyai banyak peluang untuk memenuhi kebutuhan negara-negara yang jumlah trade balance nya negative (peluang ekspor), salah satunya ke negara USA """)

    with st.expander("Lihat Data Tubular"):
        
         st.dataframe(df)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header('Perkembangan Ekspor Impor Essential Oil di Indonesia')
    # Data Exim Indonesia
    df2 = pd.read_csv('./capstone_project_farhan_sn/exim_val_net.csv')

    CURR_YEAR = max(df2['tahun'])
    PREV_YEAR = CURR_YEAR - 1

    data_exim = pd.pivot_table(
        data=df2,
        index='tahun',
        aggfunc={
            'netweight_import_kg':'sum',
            'value_import_usd':'sum',
            'netweight_export_kg':'sum',
            'value_export_usd':'sum',
            'ctr_id':pd.Series.nunique,
            'ctr':pd.Series.nunique
        }
    ).reset_index()
    # st.dataframe(data_exim)

    # selectbox memungkinkan kita untuk memilih input dari dropdown
    parameter_alpha = st.selectbox(
        "Pilih Tahun",
        options=[2019, 2020, 2021, 2022, 2023],  
        index=4  
    )

    # Update CURR_YEAR dan PREV_YEAR berdasarkan slider
    CURR_YEAR = parameter_alpha
    PREV_YEAR = CURR_YEAR - 1

    # Definisi fungsi format_big_number
    def format_big_number(num):
        if num <= 100000000:
            return f"{num}kg"
        if num >= 1e6:
            return f"USD {num / 1e6:.2f} Mio"
        elif num >= 1e3:
            return f"{num / 1e3:.2f} K"
        else:
            return f"{num:.2f}"

    # Bagian untuk menampilkan metric
    val_exp, val_imp, net_exp, net_imp = st.columns(4)

    with val_exp:
        curr_exp = data_exim.loc[data_exim['tahun']==CURR_YEAR, 'value_export_usd'].values[0] if CURR_YEAR in data_exim['tahun'].values else 0
        prev_exp = data_exim.loc[data_exim['tahun']==PREV_YEAR, 'value_export_usd'].values[0] if PREV_YEAR in data_exim['tahun'].values else 0
        exp_diff_pct = 100.0 * (curr_exp - prev_exp) / prev_exp if prev_exp != 0 else 0
        st.metric("Value Export", value=format_big_number(curr_exp), delta=f'{exp_diff_pct:.2f}%')

    with val_imp:
        curr_imp = data_exim.loc[data_exim['tahun']==CURR_YEAR, 'value_import_usd'].values[0] if CURR_YEAR in data_exim['tahun'].values else 0
        prev_imp = data_exim.loc[data_exim['tahun']==PREV_YEAR, 'value_import_usd'].values[0] if PREV_YEAR in data_exim['tahun'].values else 0
        imp_diff_pct = 100.0 * (curr_imp - prev_imp) / prev_imp if prev_imp != 0 else 0
        st.metric("Value Import", value=format_big_number(curr_imp), delta=f'{imp_diff_pct:.2f}%')

    with net_exp:
        curr_net_exp = data_exim.loc[data_exim['tahun']==CURR_YEAR, 'netweight_export_kg'].values[0] if CURR_YEAR in data_exim['tahun'].values else 0
        prev_net_exp = data_exim.loc[data_exim['tahun']==PREV_YEAR, 'netweight_export_kg'].values[0] if PREV_YEAR in data_exim['tahun'].values else 0
        exp_net_diff_pct = 100.0 * (curr_net_exp - prev_net_exp) / prev_net_exp if prev_net_exp != 0 else 0
        st.metric("Netweight Export", value=format_big_number(curr_net_exp), delta=f'{exp_net_diff_pct:.2f}%')

    with net_imp:
        curr_net_imp = data_exim.loc[data_exim['tahun']==CURR_YEAR, 'netweight_import_kg'].values[0] if CURR_YEAR in data_exim['tahun'].values else 0
        prev_net_imp = data_exim.loc[data_exim['tahun']==PREV_YEAR, 'netweight_import_kg'].values[0] if PREV_YEAR in data_exim['tahun'].values else 0
        imp_net_diff_pct = 100.0 * (curr_net_imp - prev_net_imp) / prev_net_imp if prev_net_imp != 0 else 0
        st.metric("Netweight Import", value=format_big_number(curr_net_imp), delta=f'{imp_net_diff_pct:.2f}%')

    st.markdown("""Berdasarkan data ekspor impor dari Badan Pusat Statistik sendiri pergerakan value ekspor Essential Oil (HS 33) sempat mengalami penurunan pada tahun 2022, namun pada tahun yang
                sama netweight ekspor mengalami kenaikan, itu berarti harga pada tahun itu memang cukup rendah yang membuat value ekspor nya justru turun. Pada tahun 2023 sendiri baik value maupun netweight
                ekspor mengalami kenaikan, namun juga diikuti dengan kenaikan dalam impor nya. Ini berarti Indonesia masih __Negatif__ dalam hal trade balance. Padahal 10 besar negara importir komoditi HS 33 dari Indonesia
                beberapa diantaranya merupakan negara yang memiliki persentase tinggi dalam hal _pangsa pasar impor dunia (%)_ untuk komoditas ini __(USA 21.4%, France 8.2%, India 6.1%, China 4.9%)__""")

    # Kelompokkan data berdasarkan negara dan hitung total nilai ekspor
    total_export_per_country = df2.groupby('ctr').agg({'value_export_usd': 'sum'}).reset_index()

    # Urutkan hasilnya berdasarkan 'value_export_usd' untuk mendapatkan ranking ekspor
    total_export_per_country = total_export_per_country.sort_values(by='value_export_usd', ascending=False)
    total_export_per_country['rank'] = total_export_per_country['value_export_usd'].rank(method='dense', ascending=False)

    # Mengelompokkan data berdasarkan negara dan tahun, dan menghitung total nilai ekspor untuk setiap kelompok
    df2_grouped = df2.groupby(['ctr', 'tahun']).agg({'value_export_usd': 'sum'}).reset_index()

    # Gabungkan df2_grouped dengan total_export_per_country untuk mendapatkan ranking
    df2_grouped_ranked = df2_grouped.merge(total_export_per_country[['ctr', 'rank']], on='ctr', how='left')

    # Widget multiselect untuk memilih negara
    selected_countries = st.multiselect('Pilih Negara', total_export_per_country['ctr'], default=total_export_per_country['ctr'][:10])  # Defaultnya adalah 10 negara teratas

    # Filter df2_grouped_ranked untuk hanya menyertakan negara yang dipilih
    df2_selected_countries_ranked = df2_grouped_ranked[df2_grouped_ranked['ctr'].isin(selected_countries)]

    # Buat chart dengan Altair menggunakan data yang sudah diurutkan
    chart = alt.Chart(df2_selected_countries_ranked).mark_line(point=True).encode(
        x=alt.X('tahun:N', axis=alt.Axis(title='Tahun', labelAngle=0)),
        y=alt.Y('value_export_usd:Q', axis=alt.Axis(title='Nilai Ekspor (USD)')),
        color=alt.Color('ctr:N', sort=alt.EncodingSortField(field='rank', op='min', order='ascending'), legend=alt.Legend(title="Negara")),
        tooltip=['ctr', 'tahun', 'value_export_usd']
    ).properties(
        title='Indonesia Essential Oil Importers',
        width=300,
        height=400
    )
    st.altair_chart(chart, use_container_width=True)
    # Penjabaran tentang perkembangan
    st.markdown("""10 negara paling banyak meng impor Essential Oil dari Indonesia sebagian besar berasal dari Asia. Namun perkembangannya pun fluktuatif dan hanya beberapa negara
                yang mengalami kenaikan yang stabil, salah satunya United Arab Emirates yang saat ini industri parfume nya sedang sangat ramai. Ini bisa menjadi salah satu peluang bagi Indonesia.""")
    
    with st.expander("Data yang digunakan"):
        st.markdown("**Data Ekspor Impor Badan Pusat Statistik (BPS) (HS 33) 2019 - 2023**: (https://www.bps.go.id/id/exim)")
        st.markdown("<hr>", unsafe_allow_html=True)
        st.dataframe(df2)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.header('Index Spesialisasi Perdagangan (ISP)')
    col1, col2= st.columns(2)
    with col1:
        st.latex(r'''
        S_i = \frac{{X_i - M_i}}{{X_i + M_i}}
        ''')
        st.markdown('''
        Dimana:\n
        - $X_i$ adalah nilai ekspor komoditi $i$
        - $M_i$ adalah nilai impor komoditi $i$
        ''')
    with col2:
        st.markdown('''
        <h2>ISP Essential Oil : -0.165</h2>
        ''', unsafe_allow_html=True)
    with st.expander("Penjelasan ISP"):
        st.markdown("""Index Spesialis Perdagangan (ISP) merupakan ukuran yang digunakan untuk menganalisis posisi atau tahapan
                    perkembangan suatu produk sehingga dapat dilihat kecenderungan suatu negara sebgai eksportir atau importir
                    Nilai ISP ini mempunyai kisaran antara -1 sampai dengan +1. Jika nilanya positif diatas 0 sampai 1, maka komoditi bersangkutan dikatakan mempunyai
                    daya saing yang kuat atau negara yang bersangkutan cenderung sebagai pengekspor dari komoditi tersebut. Berdasarkan nilai yang didapatkan Indonesia
                    masih memiliki nilai (-), padahal posisi nya adalah 10 besar peng ekspor di komoditi ini. Lalu apa saja kendala yang kemungkinan dihadapi?""")


with tab2:
    st.header("Patchouli and Parfume")
#Luas lahan dan produktivitas
    df3 = pd.read_csv('./capstone_project_farhan_sn/luas_lahan_produktivitas.csv')
    import plotly.express as px

    col1, col2= st.columns(2)  # Membuat dua kolom

    # Menggunakan Plotly Express untuk membuat map chart
    fig = px.scatter_geo(df3,
                        lat='latitude',
                        lon='longitude',
                        size="luas_areal_tanam_2023",
                        color="produksi_ton_2023",
                        hover_name="provinsi",
                        projection="natural earth",
                        title="Provinsi Sentra Nilam (Patchouli) 2023")


    fig.update_traces(
        marker=dict(line=dict(width=1, color='DarkSlateGrey')),  
        selector=dict(mode='markers+text')  
    )
    
    fig.update_traces(
        hoverinfo='all',
        hovertemplate="<b>%{hovertext}</b><br><br>Luas Areal Tanam 2023: %{marker.size:,} Ha<br>Produksi 2023 (Ton): %{marker.color:,} Ton"
    )
    # Menyesuaikan tampilan peta untuk difokuskan ke Indonesia dan mengurangi zoom
    fig.update_geos(
        visible=False,
        showcountries=True,
        countrycolor="Black",
        showsubunits=True,
        subunitcolor="Blue",
        center=dict(lat=-2.548926, lon=118.0148634),  
        projection_scale=3  
    )
    fig.update_layout(
        width=700,  
        height=500,  
        geo=dict(
            scope='asia',
            showlakes=True,
            lakecolor='Blue'
        ),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    df4 = pd.read_csv('./capstone_project_farhan_sn/harga_minyak_nilam.csv')

    # Membuat bar chart
    bar_harga = alt.Chart(df4).mark_bar(opacity=0.7, color='green').encode(
        x=alt.X('Tahun:N', axis=alt.Axis(title='', labelAngle=0)), 
        y=alt.Y('Average:Q', axis=alt.Axis(title='Harga')),
    )
    # Membuat line chart 
    chart_harga = alt.Chart(df4).mark_line(point=True).encode(
        x=alt.X('Tahun:O', title='Tahun'),  
        y=alt.Y('Average:Q', title='Harga Rata-Rata Minyak Nilam (Rp/Kg)'),
        tooltip=['Tahun', 'Average']
    ).properties(
        title='Harga Rata-Rata Minyak Nilam per Tahun',
        width=400,
        height=400
    )
    # Menggabungkan bar dan line chart
    harga_chart = (bar_harga + chart_harga)

    col1, spacer, col2 = st.columns([1, 0.1, 1])  

    with col1:
        st.plotly_chart(fig, use_container_width=True)  

    with spacer:
        st.write("")  

    with col2:
        st.altair_chart(harga_chart, use_container_width=True)

    st.markdown("""Salah satu jenis tanaman yang bisa menghasilkan Essential Oil adalah Patchouli (Nilam). Kualitas Patchouli dari Indonesia (khususnya Aceh) sudah sangat terkenal di seluruh dunia,
                bahkan salah satu brand internasional __Dior__ melalui laman Instagram nya pernah menunjukkan bahwa salah satu parfume best seller mereka _Dior Sauvage_ menggunakan
                patchouli yang berasal dari Indonesia ([Link video](https://www.instagram.com/reel/CiKpDaljEdQ/?utm_source=ig_web_copy_link)). Berdasarkan persebaran areal tanam dan produksinya sendiri
                __Provinsi Sumatera dan Sulawesi__ menjadi daerah dengan luas areal dan produksi terbesar di Indonesia. Menariknya berdasarkan data dari [Direktorat Jenderal Perkebunan Kementerian Pertanian Indonesia](https://ditjenbun.pertanian.go.id/?publikasi=buku-statistik-perkebunan-2021-2023) seluruh kegiatan perkembangan komoditas Patchouli (Nilam)
                di Indonesia dilakukan lewat __Perkebunan Rakyat__ (tidak ada milik swasta maupun pemerintah) dengan total __78547 Ha__ per Desember 2023. Perkembangan luas areal, produksi dan produktivitas cenderung fluktuatif, hal tersebut salah satunya dikarenakan harga pasar yang jika dibandingkan dengan komoditi lain memang bisa dibilang cukup rendah.
                __Apa upaya yang bisa dilakukan saat ini?__""")

    #Membuat barchart areal tanam
    # Mengagregasi data untuk mendapatkan total luas areal tanam setiap tahun
    total_per_tahun = {
        'Tahun': ['2020', '2021', '2022', '2023'],
        'Total Luas Areal Tanam': [
            df3['luas_areal_tanam_2020'].sum(),
            df3['luas_areal_tanam_2021'].sum(),
            df3['luas_areal_tanam_2022'].sum(),
            df3['luas_areal_tanam_2023'].sum(),
        ]
    }
    total_df = pd.DataFrame(total_per_tahun)

    col1, col2, col3 = st.columns(3)
    # Membuat bar chart
    bar = alt.Chart(total_df).mark_bar(opacity=0.7, color='red').encode(
        x=alt.X('Tahun:N', axis=alt.Axis(title='', labelAngle=0)),  # Membuat label sumbu x horizontal
        y=alt.Y('Total Luas Areal Tanam:Q', axis=alt.Axis(title='Total Luas Areal Tanam')),
    )

    # Membuat line chart
    line = alt.Chart(total_df).mark_line(color='blue').encode(
        x='Tahun:N',
        y='Total Luas Areal Tanam:Q',
    )

    # Menambahkan point pada line chart
    points = line.mark_point(color='blue', size=50)

    # Menggabungkan bar dan line chart
    areal_tanam_chart = (bar + line + points).properties(
        width=400, 
        height=300,
        title=alt.TitleParams(
            text='Luas Areal (Ha)',  # Judul chart
            align='center',  # Menempatkan judul di tengah
            fontSize=16  # Ukuran font judul
        )
    )

    # Membuat barchart produksi
    # Mengagregasi data untuk mendapatkan total luas areal tanam setiap tahun
    total_produksi_per_tahun = {
        'Tahun': ['2020', '2021', '2022', '2023'],
        'Total Produksi': [
            df3['produksi_ton_2020'].sum(),
            df3['produksi_ton_2021'].sum(),
            df3['produksi_ton_2022'].sum(),
            df3['produksi_ton_2023'].sum(),
        ]
    }
    total_df = pd.DataFrame(total_produksi_per_tahun)
    # Membuat bar chart
    bar = alt.Chart(total_df).mark_bar(opacity=0.7, color='red').encode(
        x=alt.X('Tahun:N', axis=alt.Axis(title='', labelAngle=0)),  # Membuat label sumbu x horizontal
        y=alt.Y('Total Produksi:Q', axis=alt.Axis(title='Produksi (Ton)')),
    )
    # Membuat line chart
    line = alt.Chart(total_df).mark_line(color='blue').encode(
        x='Tahun:N',
        y='Total Produksi:Q',
    )
    # Menambahkan point pada line chart
    points = line.mark_point(color='blue', size=50)
    # Menggabungkan bar dan line chart
    chart_produksi = (bar + line + points).properties(
        width=400, 
        height=300,
        title=alt.TitleParams(
            text='Total Produksi (Ton)',
            align='center', 
            fontSize=16 
        )
    )

    # Membuat barchart produktivitas
    total_produktivitas = {
        'Tahun': ['2020', '2021', '2022', '2023'],
        'Total Produktivitas': [
            df3['produktivitas_2020'].sum(),
            df3['produktivitas_2021'].sum(),
            df3['produktivitas_2022'].sum(),
            df3['produktivitas_2023'].sum(),
        ]
    }
    produktivitas = pd.DataFrame(total_produktivitas)
    # Membuat bar chart
    bar_produktivitas = alt.Chart(produktivitas).mark_bar(opacity=0.7, color='red').encode(
        x=alt.X('Tahun:N', axis=alt.Axis(title='', labelAngle=0)),  # Membuat label sumbu x horizontal
        y=alt.Y('Total Produktivitas:Q', axis=alt.Axis(title='Produktivitas (Kg/Ha)')),
    )
    # Membuat line chart
    line_produktivitas = alt.Chart(produktivitas).mark_line(color='blue').encode(
        x='Tahun:N',
        y='Total Produktivitas:Q',
    )
    # Menambahkan point pada line chart
    points_produktivitas = line_produktivitas.mark_point(color='blue', size=50)
    # Menggabungkan bar dan line chart
    chart_produktivitas = (bar_produktivitas + line_produktivitas + points_produktivitas).properties(
        width=400, 
        height=300,
        title=alt.TitleParams(
            text='Produktivitas (Kg/Ha)',
            align='center', 
            fontSize=16 
        )
    )
    col1, spacer, col2, spacer, col3 = st.columns([1, 0.1, 1, 0.1, 1])  # Angka 0.1 untuk spacer, menyesuaikan sesuai kebutuhan

    with col1:
        st.altair_chart(areal_tanam_chart, use_container_width=True)  # Menampilkan chart pertama di kolom pertama

    with spacer:
        st.write("")  # Kolom spacer, bisa juga menggunakan st.empty()

    with col2:
        st.altair_chart(chart_produksi, use_container_width=True)

    with spacer:
        st.write("")  # Kolom spacer, bisa juga menggunakan st.empty()

    with col3:
        st.altair_chart(chart_produktivitas, use_container_width=True)

    with st.expander("Data Tubular"):
        st.dataframe(df3)

    col1, col2 = st.columns(2)
    df5 = pd.read_csv('./capstone_project_farhan_sn/penjualan_ecommerce.csv')
    # Menghitung total penjualan untuk local dan internasional
    # Menghitung total penjualan untuk local dan internasional
    df_sales = df5.groupby('brand')['sold'].sum().reset_index()

    # Menghitung total penjualan keseluruhan untuk menemukan persentase
    total_sales = df_sales['sold'].sum()
    df_sales['percentage'] = (df_sales['sold'] / total_sales) * 100

    # Membuat pie chart
    pie_chart = alt.Chart(df_sales).mark_arc().encode(
        theta=alt.Theta(field='sold', type='quantitative', stack=True),
        color=alt.Color(field='brand', type='nominal', legend=alt.Legend(title="Brand Type")),
        tooltip=[alt.Tooltip(field='brand', type='nominal', title='Brand'),
                alt.Tooltip(field='sold', type='quantitative', title='Sold'),
                alt.Tooltip(field='percentage', type='quantitative', title='Percentage', format='.2f')]
    ).properties(
        title="Perbandingan Persentase Penjualan Brand Local vs Internasional"
    )

    #Tabel penjualan brand local
    # Filter untuk mendapatkan hanya penjualan dari brand local
    df_local_brands = df5[df5['brand'] == "local"]

    # Mengelompokkan data berdasarkan 'shop' dan menghitung total 'sold'
    df_shop_sales = df_local_brands.groupby('shop')['sold'].sum().reset_index()

    # Mengurutkan df_shop_sales berdasarkan 'sold' secara descending dan mengambil 10 teratas
    df_top_shops = df_shop_sales.sort_values(by='sold', ascending=False).head(10)

    # Membuat chart horizontal besar dengan Altair menggunakan data yang sudah diurutkan dan dibatasi
    chart = alt.Chart(df_top_shops).mark_bar().encode(
        y=alt.Y('shop:N', title='Brand', sort='-x'),  # Mengurutkan axis y berdasarkan nilai x secara descending
        x=alt.X('sold:Q', title='Total Sold'),
        color=alt.Color('shop:N', legend=alt.Legend(title="Shop"), sort=alt.EncodingSortField(field="sold", order="descending"))
    ).properties(
        title="10 Brand Local Dengan Penjualan Terbanyak",
        width=600,  # Lebar chart
        height=400  # Tinggi chart
    )

    # Chart perbandingan harga
    # Menghitung rata-rata harga untuk brand lokal dan internasional
    avg_price_local = df5[df5['brand'] == 'local']['price'].mean()
    avg_price_international = df5[df5['brand'] == 'international']['price'].mean()

    # Membuat dataframe baru untuk rata-rata harga
    df_avg_prices = pd.DataFrame({
        'brand_type': ['Local', 'International'],
        'average_price': [avg_price_local, avg_price_international]
    })
    chart_parfume = alt.Chart(df_avg_prices).mark_bar().encode(
        x=alt.X('brand_type:N', title='Brand Type', axis=alt.Axis(labelAngle=0)), 
        y=alt.Y('average_price:Q', title='Average Price'),
        color=alt.Color('brand_type:N', legend=alt.Legend(title="Brand Type"))
    ).properties(
        title="Average Price of Perfume by Brand Type",
        width=600,  # Lebar chart
        height=400  # Tinggi chart
    )
    col1, spacer, col2 = st.columns([1, 0.1, 1])

    with col1:
        st.altair_chart(pie_chart, use_container_width=True)

    with spacer:
        st.write("")

    with col2:
        st.altair_chart(chart, use_container_width=True)

    col1, col2 = st.columns(2)
    col1, spacer, col2 = st.columns([1, 0.1, 1])

    with col1:
       st.altair_chart(chart_parfume, use_container_width=True)

    with spacer:
        st.write("")

    with col2:
        st.write("""Salah satu upaya yang dapat dilakukan adalah mendorong program hilirisasi industri. Di Indonesia sendiri pemanfaatan Essential Oil yang sedang 
                 meningkat trend penjualannya adalah sebagai __Parfume__. Berdasarkan data penjualan e-commerce per 17 Februari 2024 __local brand__ menjadi pilihan utama para pembeli
                 dibandingkan international brand. Keunggulan utama dari local brand sendiri adalah __harga yang jauh lebih murah__ dibandingkan dengan international brand. Bahkan beberapa
                 local brand parfume dari Indonesia sudah mulai melebarkan sayap di pasar internasional. Ini bisa menjadi peluang yang sangat baik jika didukung dengan pengembangan kualitas yang semakin baik.""")
