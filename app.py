import streamlit as st
from converter import convert_all, normalize_ext
from pathlib import Path
import zipfile
import io

st.title("File Converter Tool 📁")

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
    st.write(f"📤 Uploaded {len(uploaded_files)} file(s):")
    for uploaded_file in uploaded_files:
        st.write(f"  • {uploaded_file.name}")

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
            
            # Single file: direct download
            if len(converted_files) == 1:
                with open(converted_files[0], "rb") as f:
                    st.download_button(
                        label=f"📥 Download {converted_files[0].name}",
                        data=f,
                        file_name=converted_files[0].name
                    )
            # Multiple files: zip download
            else:
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                    for file_path in converted_files:
                        zip_file.write(file_path, file_path.name)
                
                st.download_button(
                    label=f"📦 Download All ({len(converted_files)} files as ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name=f"converted_files.zip",
                    mime="application/zip"
                )
        
        if errors:
            st.error("⚠️ Some files failed:")
            for error in errors:
                st.write(f"  • {error}")
