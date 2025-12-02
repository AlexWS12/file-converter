import streamlit as st
from converter import convert_all, normalize_ext
from pathlib import Path

st.title("File Converter Tool")

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

# Upload only files that match the chosen input format
uploaded_file = st.file_uploader(
    f"Upload a .{from_ext} file",
    type=[from_ext]
)

if uploaded_file:
    st.write(f"Uploaded: {uploaded_file.name}")

    # Save uploaded file temporarily
    upload_dir = Path("uploaded_files")
    upload_dir.mkdir(exist_ok=True)
    src_path = upload_dir / uploaded_file.name

    with open(src_path, "wb") as f:
        f.write(uploaded_file.read())

    if st.button("Convert"):
        try:
            # Use existing converter
            convert_all(str(upload_dir), from_ext, to_ext)

            # Make output filename with new extension
            dst_suffix = normalize_ext(to_ext)
            dst_path = src_path.with_suffix(dst_suffix)

            st.success(f"Conversion successful: {dst_path.name}")

            # Let user download the result
            with open(dst_path, "rb") as f:
                st.download_button(
                    label="Download converted file",
                    data=f,
                    file_name=dst_path.name
                )

        except KeyError:
            st.error("This conversion is not available yet.")
        except Exception as e:
            st.error(str(e))
