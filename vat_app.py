 import streamlit as st

st.title("🛒แอปพลิเคชั่นคำนวณราคาสินค้ารวม VAT 7%")

price = st.number_input("กรอกราคาสินค้า (บาท):", value=0.0)

st.header(f"• ภาษีมูลค่าเพิ่ม (VAT 7%): **{vat:.2f}** บาท")

net_price = price - vat

vat = price * 0.07

st.header(f"• ราคาสุทธิ: {net_price:.2f} บาท")

st.divider()

st.write("นางสาวทับทิม คำป้อ เลขที่ 43 ม.4/7")
