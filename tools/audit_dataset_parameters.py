import os
import sys
import time
import glob
import json
import cv2
import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def audit():
    print("=" * 70)
    print("🔍 BẮT ĐẦU KIỂM ĐỊNH TOÀN DIỆN 100% THÔNG SỐ DỮ LIỆU TCGA-LGG")
    print("=" * 70)
    start_time = time.time()
    
    # 1. Đường dẫn dữ liệu
    img_dir = os.path.join("data", "full", "images")
    mask_dir = os.path.join("data", "full", "masks")
    meta_path = os.path.join("data", "full", "metadata.csv")
    clinical_path = os.path.join("data", "full", "clinical_data.csv")
    
    # Kiểm tra tồn tại thư mục và tệp
    for p, name in [(img_dir, "Thư mục ảnh"), (mask_dir, "Thư mục mặt nạ"), 
                    (meta_path, "Metadata CSV"), (clinical_path, "Clinical CSV")]:
        if not os.path.exists(p):
            print(f"❌ LỖI NGHIÊM TRỌNG: Không tìm thấy {name} tại {p}")
            return
            
    # 2. Kiểm tra tệp tin trên đĩa
    print("\n[Giai đoạn 1/4] Kiểm tra tệp tin vật lý trên ổ đĩa...")
    img_files = sorted([f for f in os.listdir(img_dir) if f.endswith(".png")])
    mask_files = sorted([f for f in os.listdir(mask_dir) if f.endswith(".png")])
    
    print(f"  + Số lượng tệp ảnh (.png):   {len(img_files):,} tệp")
    print(f"  + Số lượng tệp mặt nạ (.png): {len(mask_files):,} tệp")
    
    disk_1to1_mismatches = 0
    for img_f in img_files:
        expected_mask = img_f.replace(".png", "_mask.png")
        if not os.path.exists(os.path.join(mask_dir, expected_mask)):
            disk_1to1_mismatches += 1
            
    print(f"  + Số cặp ảnh-mặt nạ không khớp: {disk_1to1_mismatches} (Kỳ vọng: 0)")
    
    # 3. Quét kiểm định 100% 3,929 ảnh mặt nạ trên đĩa
    print("\n[Giai đoạn 2/4] Đang quét và đo đạc lại 100% mặt nạ Ground Truth trên đĩa...")
    t_scan = time.time()
    
    def process_mask_file(fname):
        fpath = os.path.join(mask_dir, fname)
        sample_id = fname.replace("_mask.png", "")
        mask = cv2.imread(fpath, cv2.IMREAD_GRAYSCALE)
        if mask is None:
            return sample_id, -1, -1, False, "CANNOT_READ"
        h, w = mask.shape
        if h != 256 or w != 256:
            return sample_id, -1, -1, False, f"WRONG_SHAPE_{h}x{w}"
        tumor_px = int(np.sum(mask > 0))
        tumor_ratio = round((tumor_px / (h * w)) * 100, 4)
        has_tumor = tumor_px > 0
        return sample_id, tumor_px, tumor_ratio, has_tumor, "OK"
        
    actual_results = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(process_mask_file, mf) for mf in mask_files]
        for f in futures:
            sid, t_px, t_ratio, has_t, status = f.result()
            actual_results[sid] = {
                "tumor_pixels": t_px,
                "tumor_ratio": t_ratio,
                "has_tumor": has_t,
                "status": status
            }
            
    print(f"  + Hoàn thành quét 100% ({len(actual_results):,} mặt nạ) trong {time.time() - t_scan:.2f}s.")
    
    # 4. Đối soát từng dòng với data/full/metadata.csv
    print("\n[Giai đoạn 3/4] Đối soát dòng-theo-dòng với metadata.csv...")
    df_meta = pd.read_csv(meta_path)
    print(f"  + Kích thước metadata.csv: {df_meta.shape[0]:,} dòng x {df_meta.shape[1]} cột")
    
    mismatch_pixel_count = 0
    mismatch_ratio_count = 0
    mismatch_label_count = 0
    missing_in_meta = 0
    
    for sid, act in actual_results.items():
        row = df_meta[df_meta['sample_id'] == sid]
        if row.empty:
            missing_in_meta += 1
            continue
        row = row.iloc[0]
        # Kiểm tra pixel
        if row['tumor_area_pixels'] != act['tumor_pixels'] or row['tumor_pixels'] != act['tumor_pixels']:
            mismatch_pixel_count += 1
        # Kiểm tra tỷ lệ %
        if abs(row['tumor_ratio_percent'] - act['tumor_ratio']) > 0.001:
            mismatch_ratio_count += 1
        # Kiểm tra nhãn has_tumor
        if bool(row['has_tumor']) != act['has_tumor']:
            mismatch_label_count += 1
            
    print(f"  + Sai lệch pixel khối u:       {mismatch_pixel_count} dòng (Kỳ vọng: 0)")
    print(f"  + Sai lệch tỷ lệ phần trăm:     {mismatch_ratio_count} dòng (Kỳ vọng: 0)")
    print(f"  + Sai lệch phân loại có/không u: {mismatch_label_count} dòng (Kỳ vọng: 0)")
    print(f"  + Mẫu bị thiếu trong metadata:  {missing_in_meta} dòng (Kỳ vọng: 0)")
    
    # 5. Kiểm tra 18 cột lâm sàng đã ghép
    print("\n[Giai đoạn 4/4] Kiểm tra tính nhất quán của 18 thuộc tính lâm sàng...")
    df_clin = pd.read_csv(clinical_path)
    print(f"  + Bảng lâm sàng độc lập (clinical_data.csv): {len(df_clin)} bệnh nhân x {df_clin.shape[1]} cột")
    
    clin_cols = [
        'gender', 'age_at_initial_pathologic', 'histological_type', 
        'neoplasm_histologic_grade', 'tumor_location', 'tumor_tissue_site', 
        'laterality', 'death01'
    ]
    for c in clin_cols:
        if c in df_meta.columns:
            non_null = df_meta[c].notna().sum()
            print(f"  + Cột '{c}': Có mặt | {non_null:,}/{len(df_meta):,} lát ({non_null/len(df_meta)*100:.1f}% điền đầy)")
        else:
            print(f"  + Cột '{c}': ❌ THIẾU")
            
    # 6. Thống kê số liệu phân nhóm thực tế
    print("\n" + "=" * 70)
    print("📊 BẢNG TỔNG HỢP CÁC THÔNG SỐ ĐO ĐẠC THỰC TẾ TRÊN TOÀN BỘ DỮ LIỆU")
    print("=" * 70)
    total_slices = len(df_meta)
    num_pts = df_meta['patient_id'].nunique()
    pos_df = df_meta[df_meta['has_tumor']]
    neg_df = df_meta[~df_meta['has_tumor']]
    
    small_u = pos_df[pos_df['tumor_ratio_percent'] < 1.5]
    med_u = pos_df[(pos_df['tumor_ratio_percent'] >= 1.5) & (pos_df['tumor_ratio_percent'] <= 5.0)]
    large_u = pos_df[pos_df['tumor_ratio_percent'] > 5.0]
    
    stats_data = {
        "Tong_So_Lat_Cat": total_slices,
        "Tong_So_Benh_Nhan": num_pts,
        "So_Lat_Co_U": len(pos_df),
        "Ty_Le_Lat_Co_U_Pct": round(len(pos_df) / total_slices * 100, 2),
        "So_Lat_Nao_Lanh": len(neg_df),
        "Ty_Le_Lat_Nao_Lanh_Pct": round(len(neg_df) / total_slices * 100, 2),
        "U_Nho_Duoi_1_5Pct": len(small_u),
        "U_Trung_Binh_1_5_Den_5Pct": len(med_u),
        "U_Lon_Tren_5Pct": len(large_u),
        "Dien_Tich_U_Min_Px": int(pos_df['tumor_area_pixels'].min()),
        "Dien_Tich_U_Max_Px": int(pos_df['tumor_area_pixels'].max()),
        "Dien_Tich_U_Mean_Px": round(float(pos_df['tumor_area_pixels'].mean()), 2),
        "Dien_Tich_U_Median_Px": float(pos_df['tumor_area_pixels'].median()),
        "Ty_Le_U_Min_Pct": float(pos_df['tumor_ratio_percent'].min()),
        "Ty_Le_U_Max_Pct": float(pos_df['tumor_ratio_percent'].max()),
        "Ty_Le_U_Mean_Pct": round(float(pos_df['tumor_ratio_percent'].mean()), 4),
        "Ty_Le_U_Median_Pct": float(pos_df['tumor_ratio_percent'].median()),
    }
    
    for k, v in stats_data.items():
        print(f"  {k:30}: {v}")
        
    print(f"\n⏱️ Tổng thời gian kiểm định toàn bộ: {time.time() - start_time:.2f} giây.")
    print("=" * 70)
    
    # Lưu kết quả kiểm định dạng JSON
    with open("tools/audit_summary.json", "w", encoding="utf-8") as f:
        json.dump(stats_data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    audit()
