import streamlit as st
from converter import convert_all, normalize_ext
from pathlib import Path
import zipfile
import io
import pandas as pd
from PIL import Image
import json
import yaml

def format_size(bytes):
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024
    return f"{bytes:.1f} TB"

def preview_file(uploaded_file, ext):
    """Show preview based on file type."""
    try:
        # Text-based formats
        if ext in ["txt", "md", "html", "xml", "yaml", "yml", "toon"]:
            content = uploaded_file.read().decode("utf-8")
            uploaded_file.seek(0)  # Reset for later use
            st.code(content[:1000], language=ext if ext != "yml" else "yaml")
            if len(content) > 1000:
                st.caption(f"Showing first 1000 characters of {len(content)} total")
        
        # JSON
        elif ext == "json":
            content = uploaded_file.read().decode("utf-8")
            uploaded_file.seek(0)
            data = json.loads(content)
            st.json(data)
        
        # CSV
        elif ext == "csv":
            df = pd.read_csv(uploaded_file)
            uploaded_file.seek(0)
            st.dataframe(df.head(10))
            if len(df) > 10:
                st.caption(f"Showing first 10 rows of {len(df)} total")
        
        # Images
        elif ext in ["png", "jpg", "jpeg", "webp"]:
            img = Image.open(uploaded_file)
            uploaded_file.seek(0)
            st.image(img, caption=f"{img.size[0]}x{img.size[1]} pixels", use_container_width=True)
        
        # PDF
        elif ext == "pdf":
            st.info("📄 PDF preview not available. File ready for conversion.")
        
        # DOCX
        elif ext == "docx":
            st.info("📝 DOCX preview not available. File ready for conversion.")
        
        # Audio
        elif ext in ["mp3", "wav"]:
            uploaded_file.seek(0)
            st.audio(uploaded_file, format=f"audio/{ext}")
        
        # NPY
        elif ext == "npy":
            st.info("🔢 NumPy array preview not available. File ready for conversion.")
        
        else:
            st.info("Preview not available for this format.")
    
    except Exception as e:
        st.warning(f"Could not preview: {str(e)}")

st.title("File Converter Tool 📁")

# Dark mode toggle button
col1, col2 = st.columns([6, 1])
with col2:
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    
    if st.button("🌙" if not st.session_state.dark_mode else "☀️"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# Tab selection
tab1, tab2 = st.tabs(["📁 Convert Files", "📦 Extract ZIP"])

with tab2:
    st.subheader("ZIP File Extractor")
    st.write("Upload a ZIP file to extract its contents")
    
    zip_file = st.file_uploader("Upload ZIP file", type=["zip"], key="zip_uploader")
    
    if zip_file:
        st.write(f"📦 ZIP file: **{zip_file.name}** ({format_size(zip_file.size)})")
        
        try:
            # Read ZIP file
            zip_buffer = io.BytesIO(zip_file.read())
            with zipfile.ZipFile(zip_buffer, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                
                st.success(f"Found {len(file_list)} file(s) in ZIP")
                
                # Show contents
                with st.expander("📋 ZIP Contents", expanded=True):
                    for file_name in file_list:
                        file_info = zip_ref.getinfo(file_name)
                        st.write(f"• **{file_name}** - {format_size(file_info.file_size)}")
                
                if st.button("Extract All Files"):
                    extract_dir = Path("extracted_files")
                    extract_dir.mkdir(exist_ok=True)
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    extracted_files = []
                    for i, file_name in enumerate(file_list):
                        status_text.text(f"Extracting {file_name}...")
                        zip_ref.extract(file_name, extract_dir)
                        extracted_files.append(extract_dir / file_name)
                        progress_bar.progress((i + 1) / len(file_list))
                    
                    status_text.text("✅ Extraction complete!")
                    st.success(f"Extracted {len(extracted_files)} file(s) to `extracted_files/`")
                    
                    # Download individual files
                    st.write("**Download extracted files:**")
                    cols = st.columns(min(3, len(extracted_files)))
                    
                    for i, file_path in enumerate(extracted_files):
                        if file_path.is_file():
                            with cols[i % 3]:
                                with open(file_path, "rb") as f:
                                    st.download_button(
                                        label=f"📄 {file_path.name}",
                                        data=f,
                                        file_name=file_path.name,
                                        key=f"extract_{i}_{file_path.name}",
                                        use_container_width=True
                                    )
        
        except zipfile.BadZipFile:
            st.error("❌ Invalid ZIP file")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Apply theme with custom CSS
if st.session_state.dark_mode:
    st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background-color: #0e1117;
        }
        [data-testid="stHeader"] {
            background-color: #0e1117;
        }
        .stMarkdown, .stText, p, h1, h2, h3, label {
            color: #fafafa !important;
        }
        [data-testid="stFileUploadDropzone"] {
            background-color: #262730;
            border-color: #4a4a4a;
        }
        .stButton > button {
            background-color: #262730;
            color: #fafafa;
            border: 1px solid #4a4a4a;
        }
        .stSelectbox [data-baseweb="select"] {
            background-color: #262730;
        }
        [data-testid="stExpander"] {
            background-color: #1e1e1e;
            border: 1px solid #4a4a4a;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background-color: #ffffff;
        }
        [data-testid="stHeader"] {
            background-color: #ffffff;
        }
    </style>
    """, unsafe_allow_html=True)

with tab1:
    # Let user choose the type of conversion (from -> to)
    supported_exts = [
        "md", "html",
        "csv", "json", "npy", "xml",
        "yaml", "yml",
        "png", "jpg", "jpeg", "webp",
        "txt", "docx", "pdf",
        "toon",
        "mp3", "wav"
    ]
    from_ext = st.selectbox("Convert from", supported_exts)
    to_ext = st.selectbox("Convert to", [ext for ext in supported_exts if ext != from_ext])

    # Custom drag & drop styling (only for convert tab)
    st.markdown("""
<style>
    div[data-testid="stVerticalBlock"]:has(> div > div[data-testid="stFileUploader-stFileUploaderDropzone"]) [data-testid="stFileUploadDropzone"] {
        padding: 2rem;
        border: 2px dashed #1f77b4;
        border-radius: 10px;
        text-align: center;
        transition: all 0.3s ease;
    }
    div[data-testid="stVerticalBlock"]:has(> div > div[data-testid="stFileUploader-stFileUploaderDropzone"]) [data-testid="stFileUploadDropzone"]:hover {
        border-color: #ff6b6b;
        background-color: rgba(31, 119, 180, 0.05);
    }
    #convert-dropzone [data-testid="stFileUploadDropzone"]::before {
        content: "📁 Drag & Drop or Click to Browse";
        display: block;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #1f77b4;
    }
    #convert-dropzone [data-testid="stFileUploadDropzone"]::after {
        content: "Supports multiple files";
        display: block;
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)
    
    st.markdown('<div id="convert-dropzone">', unsafe_allow_html=True)

    # Upload multiple files that match the chosen input format
    uploaded_files = st.file_uploader(
        f"Upload .{from_ext} file(s)",
        type=[from_ext],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_files:
        # Show uploaded files with sizes
        total_size = sum(f.size for f in uploaded_files)
        st.write(f"📤 Uploaded {len(uploaded_files)} file(s) • Total size: {format_size(total_size)}")
    
    with st.expander("📋 File Details", expanded=False):
        for f in uploaded_files:
            st.write(f"• **{f.name}** - {format_size(f.size)}")
    
    # Preview section with tabs
    if len(uploaded_files) == 1:
        st.subheader("Preview")
        preview_file(uploaded_files[0], from_ext)
    elif len(uploaded_files) > 1:
        st.subheader("Preview")
        tabs = st.tabs([f.name for f in uploaded_files])
        for tab, uploaded_file in zip(tabs, uploaded_files):
            with tab:
                preview_file(uploaded_file, from_ext)

    if st.button("Convert All"):
        import time
        start_time = time.time()
        
        upload_dir = Path("uploaded_files")
        upload_dir.mkdir(exist_ok=True)
        
        converted_files = []
        errors = []
        conversion_times = []

        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Save all files first
        src_paths = []
        for uploaded_file in uploaded_files:
            src_path = upload_dir / uploaded_file.name
            with open(src_path, "wb") as f:
                f.write(uploaded_file.read())
            src_paths.append(src_path)

        # Convert each file individually
        for i, src_path in enumerate(src_paths):
            try:
                file_start = time.time()
                status_text.text(f"Converting {src_path.name}...")
                
                # Get conversion function directly
                from conversions import CONVERSIONS
                from_suffix = normalize_ext(from_ext)
                to_suffix = normalize_ext(to_ext)
                func = CONVERSIONS[(from_suffix, to_suffix)]
                
                # Convert this specific file
                dst_path = src_path.with_suffix(to_suffix)
                func(src_path, dst_path)
                
                if dst_path.exists():
                    converted_files.append(dst_path)
                    file_time = time.time() - file_start
                    conversion_times.append((dst_path.name, file_time))
                
                progress_bar.progress((i + 1) / len(src_paths))

            except KeyError:
                errors.append(f"{src_path.name}: Conversion not available")
            except Exception as e:
                errors.append(f"{src_path.name}: {str(e)}")

        # Show results
        total_time = time.time() - start_time
        status_text.text(f"✅ Conversion complete in {total_time:.2f}s!")
        
        if converted_files:
            st.success(f"Successfully converted {len(converted_files)} file(s)")
            
            # Show conversion times
            if conversion_times:
                with st.expander("⏱️ Conversion Times", expanded=False):
                    for file_name, file_time in conversion_times:
                        st.write(f"• **{file_name}** - {file_time:.3f}s")
                    st.write(f"**Total time:** {total_time:.2f}s")
            
            st.subheader("Download Options")
            
            # Multiple files: show both options
            if len(converted_files) > 1:
                # ZIP download
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                    for file_path in converted_files:
                        zip_file.write(file_path, file_path.name)
                
                st.download_button(
                    label=f"📦 Download All as ZIP ({len(converted_files)} files)",
                    data=zip_buffer.getvalue(),
                    file_name=f"converted_files.zip",
                    mime="application/zip"
                )
                
                # Individual downloads
                st.write("**Or download individually:**")
                cols = st.columns(min(3, len(converted_files)))
                
                for i, file_path in enumerate(converted_files):
                    with cols[i % 3]:
                        with open(file_path, "rb") as f:
                            st.download_button(
                                label=f"📄 {file_path.name}",
                                data=f,
                                file_name=file_path.name,
                                key=f"download_{file_path.name}",
                                use_container_width=True
                            )
            
            # Single file: just direct download
            else:
                with open(converted_files[0], "rb") as f:
                    st.download_button(
                        label=f"📥 Download {converted_files[0].name}",
                        data=f,
                        file_name=converted_files[0].name
                    )
        
        if errors:
            st.error("⚠️ Some files failed:")
            for error in errors:
                st.write(f"  • {error}")
