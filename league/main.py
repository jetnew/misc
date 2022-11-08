import dearpygui.dearpygui as dpg
from util import load_data
from callbacks import update_winrate


dpg.create_context()
dpg.create_viewport(title='League', width=700, height=270)

data = load_data()
top_champions = [''] + list(data['top'].keys())
jungle_champions = [''] + list(data['jungle'].keys())
mid_champions = [''] + list(data['mid'].keys())
adc_champions = [''] + list(data['adc'].keys())
support_champions = [''] + list(data['support'].keys())


with dpg.window(tag="Window"):
    with dpg.collapsing_header(label="Matchup Winrate", default_open=True):
        with dpg.table(tag="table"):
            dpg.add_table_column(label="Role")
            dpg.add_table_column(label="Ally")
            dpg.add_table_column(label="Enemy")
            dpg.add_table_column(label="Winrate")
            with dpg.table_row(tag='top'):
                dpg.add_text("Top")
                dpg.add_combo(items=top_champions, width=-1, callback=update_winrate)
                dpg.add_combo(items=top_champions, width=-1, callback=update_winrate)
                dpg.add_text(tag='top_winrate')
            with dpg.table_row(tag='jungle'):
                dpg.add_text("Jungle")
                dpg.add_combo(items=jungle_champions, width=-1, callback=update_winrate)
                dpg.add_combo(items=jungle_champions, width=-1, callback=update_winrate)
                dpg.add_text(tag='jungle_winrate')
            with dpg.table_row(tag='mid'):
                dpg.add_text("Mid")
                dpg.add_combo(items=mid_champions, width=-1, callback=update_winrate)
                dpg.add_combo(items=mid_champions, width=-1, callback=update_winrate)
                dpg.add_text(tag='mid_winrate')
            with dpg.table_row(tag='adc'):
                dpg.add_text("ADC")
                dpg.add_combo(items=adc_champions, width=-1, callback=update_winrate)
                dpg.add_combo(items=adc_champions, width=-1, callback=update_winrate)
                dpg.add_text(tag='adc_winrate')
            with dpg.table_row(tag='support'):
                dpg.add_text("Support")
                dpg.add_combo(items=support_champions, width=-1, callback=update_winrate)
                dpg.add_combo(items=support_champions, width=-1, callback=update_winrate)
                dpg.add_text(tag='support_winrate')
    with dpg.collapsing_header(label="Statistics", default_open=True):
        with dpg.group(horizontal=True):
            dpg.add_text("Average Winrate: ")
            dpg.add_text(tag="average_winrate")
        with dpg.group(horizontal=True):
            dpg.add_text("Weighted Winrate: ")
            dpg.add_text(tag="weighted_winrate")
    dpg.add_text("Data from OP.GG")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Window", True)
dpg.start_dearpygui()
dpg.destroy_context()