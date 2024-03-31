import streamlit as st
from st_pages import Page, Section,show_pages, add_page_title

def main():
    show_pages(
        [
            Page("main_app.py",name="Home",icon="🏠"),
            Section(name="Strain Gauge Calculation"),
            Page("pages/01 calculator.py", "Calculation",icon="💪"),
            # Page("menuPages/second.py", "样例2",icon="💪"),
            # Section(name="项目相关",icon="🏠"),
            # Page("menuPages/xm.py", "项目",icon="💪"),
            # Page("menuPages/tax.py", "税率",icon="💪"),
            # # in_section=False用明确申明，该页不属于上面的菜单section子项目
            Page("pages/logout.py",name="Logout",icon="🏠",in_section=False),
        ]
        
    )    
if __name__ == '__main__':
    main()
    pass