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

# Upload multiple files that match the chosen input format
uploaded_files = st.file_uploader(
    f"Upload .{from_ext} file(s)",
    type=[from_ext],
    accept_multiple_files=True
)

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
    else:
        st.subheader("Preview")
        tabs = st.tabs([f.name for f in uploaded_files])
        for tab, uploaded_file in zip(tabs, uploaded_files):
            with tab:
                preview_file(uploaded_file, from_ext)

    if st.button("Convert All"):
        upload_dir = Path("uploaded_files")
        upload_dir.mkdir(exist_ok=True)
        
        converted_files = []
        errors = []

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
                
                progress_bar.progress((i + 1) / len(src_paths))

            except KeyError:
                errors.append(f"{src_path.name}: Conversion not available")
            except Exception as e:
                errors.append(f"{src_path.name}: {str(e)}")

        # Show results
        status_text.text("✅ Conversion complete!")
        
        if converted_files:
            st.success(f"Successfully converted {len(converted_files)} file(s)")
            
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
