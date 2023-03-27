import dearpygui.dearpygui as dpg
import os
import subprocess
import sys

def run_chatpaper_pdf(sender, data):

    pdf_dir = dpg.get_value("pdf_dir")
    pdf_path = os.path.join(pdf_dir, dpg.get_value("pdf_input"))
    if not pdf_path.endswith('.pdf'):
        pdf_path += '.pdf'

    # Do some work in the './repo' directory
    cmds = ['python', 'chat_paper.py', '--pdf_path', f'{pdf_path}', '--output_dir', f'{pdf_dir}']
    cmd = ' '.join(cmds)
    print(f'Run \n cmd:{cmd}')

    # Start the process
    process = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print("invoke_chatpaper:")
    # Read the output in real-time
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print(output.strip().decode('utf-8'))

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


dpg.create_context()
dpg.create_viewport(title='AI Research Vault', width=800, height=400)

with dpg.window(label="PDF Chatpaper", width=800, height=200) as primary_window:

    dpg.add_text("Enter PDF directory:")
    dpg.add_input_text(tag="pdf_dir", width=800)

    dpg.add_text("Enter PDF file name:")
    dpg.add_input_text(tag="pdf_input", width=800)

    dpg.add_button(label="Invoke chatpaper", callback=run_chatpaper_pdf)

    textbox_id = dpg.add_input_text(label="Output", multiline=True, height=200)
    sys.stdout.write = write_to_textbox(textbox_id)


dpg.setup_dearpygui()

dpg.show_viewport()
dpg.set_primary_window(window=primary_window, value=True)

dpg.start_dearpygui()

dpg.destroy_context()

