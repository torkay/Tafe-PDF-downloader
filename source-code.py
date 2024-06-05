import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from bs4 import BeautifulSoup
import subprocess
import io
import os
import webbrowser

# Function to download PDF file
def download_pdf(pdf_url):
    try:
        # Download PDF using curl
        subprocess.run(["curl", "-o", "downloaded_file.pdf", pdf_url], check=True)
        response = messagebox.askquestion("Download Complete", "PDF downloaded successfully! Do you want to open it?")
        if response == "yes":
            open_downloaded_pdf()
    except Exception as e:
        messagebox.showerror("Download Error", f"An error occurred while downloading PDF: {str(e)}")

# Function to parse HTML and extract PDF URL
def parse_html_and_download(html_content):
    try:
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the element containing the PDF URL
        pdf_element = soup.find('div', class_='d2l-fileviewer-pdf-pdfjs')
        if pdf_element:
            pdf_url = pdf_element.get('data-location')
            if pdf_url:
                print(f"Found PDF URL: {pdf_url}")

                # Download PDF
                download_pdf(pdf_url)
            else:
                messagebox.showerror("PDF URL Not Found", "PDF URL not found in the HTML content.")
        else:
            messagebox.showerror("PDF Viewer Element Not Found", "PDF viewer element with class 'd2l-fileviewer-pdf-pdfjs' not found.")
    except Exception as e:
        messagebox.showerror("Parsing Error", f"An error occurred while parsing HTML: {str(e)}")

# Function to handle download button click
def handle_download():
    # Get HTML content from textbox
    html_content = html_textbox.get("1.0", tk.END)

    # Call parse function
    parse_html_and_download(html_content)

# Function to handle save button click
def handle_save():
    # Get HTML content from textbox
    html_content = html_textbox.get("1.0", tk.END)

    # Save HTML content to a file
    filename = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html"), ("All files", "*.*")])
    if filename:
        try:
            with io.open(filename, "w", encoding="utf-8") as f:
                f.write(html_content)
            messagebox.showinfo("File Saved", f"HTML content saved to {filename}")
        except Exception as e:
            messagebox.showerror("Save Error", f"An error occurred while saving file: {str(e)}")

# Function to open the downloaded PDF file
def open_downloaded_pdf():
    file_path = os.path.join(os.getcwd(), "downloaded_file.pdf")
    webbrowser.open(file_path)

# Main function to create GUI
def main():
    global html_textbox

    # Create main window
    root = tk.Tk()
    root.title("HTML Parser and PDF Downloader")
    root.geometry("800x600")

    # Create a scrolled text box to paste HTML content
    html_textbox = scrolledtext.ScrolledText(root, width=100, height=30, wrap=tk.WORD)
    html_textbox.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

    # Button to download PDF
    download_button = tk.Button(root, text="Download PDF", width=15, command=handle_download)
    download_button.grid(row=1, column=0, padx=10, pady=10)

    # Button to save HTML content
    save_button = tk.Button(root, text="Save HTML", width=15, command=handle_save)
    save_button.grid(row=1, column=1, padx=10, pady=10)

    # Run the main tkinter loop
    root.mainloop()

if __name__ == "__main__":
    main()
