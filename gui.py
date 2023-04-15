import dearpygui.dearpygui as dpg
import os
import subprocess
import sys
import locale

def run_chatpaper_pdf(sender, data):

    pdf_path = dpg.get_value("pdf_input")
    pdf_path = pdf_path.replace("\\", "/")
    if not pdf_path.endswith('.pdf') and not os.path.isdir(pdf_path):
        pdf_path += '.pdf'
    pdf_dir = os.path.split(pdf_path)[0]

    # Do some work in the './repo' directory
    cmds = ['python', 'chat_paper.py', '--pdf_path', f'''{pdf_path}''', '--output_dir', f'''{pdf_dir}''']
    cmd = ' '.join(cmds)
    print(f'Run \n cmd:{cmd}')

    dpg.set_value("cmd_out", cmd)

    # Start the process
    process = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print("invoke_chatpaper...")
    # Read the output in real-time
    for output in process.stdout:
        print(output.strip().decode(system_cmd_encoding))

    for output in process.stderr:
        print(output.strip().decode(system_cmd_encoding))

    # Wait for the process to finish and get the return code
    result = process.poll()

    if result == 0:
        print("invoke_chatpaper succeeded")
    else:
        print("invoke_chatpaper failed with return code", result)


def write_to_textbox(textbox_id):
    def write(text):
        dpg.set_value(textbox_id, dpg.get_value(textbox_id) + text)
    return write


if __name__ == '__main__':

    system_cmd_encoding = locale.getpreferredencoding(False)
    print(f'system_cmd_encoding: {system_cmd_encoding}')

    dpg.create_context()
    dpg.create_viewport(title='AI Research Vault', width=800, height=400)

    with dpg.font_registry():
        with dpg.font(tag = 'CHN', file = './dpg/LXGWWenKai-Regular.ttf',
                        size = 12) as default_chn_font:
            # add the default font range
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)

    dpg.bind_font(default_chn_font)
    dpg.set_global_font_scale(1)

    with dpg.window(label="PDF Chatpaper", width=800, height=200) as primary_window:

        dpg.add_text("你好，世界！")  # Chinese text
        dpg.add_text("Enter PDF file path:")
        dpg.add_input_text(tag="pdf_input", width=800)

        dpg.add_text("Cmd:")
        dpg.add_input_text(tag="cmd_out", width=800)

        dpg.add_button(label="Invoke chatpaper", callback=run_chatpaper_pdf)

        textbox_id = dpg.add_input_text(label="Output", multiline=True, height=200)
        sys.stdout.write = write_to_textbox(textbox_id)


    dpg.setup_dearpygui()

    dpg.show_viewport()
    dpg.set_primary_window(window=primary_window, value=True)

    dpg.start_dearpygui()

    dpg.destroy_context()

