package mvcjava.controller;

import mvcjava.model.model;
import java.util.ArrayList;
import java.util.List;

public class controller {
    private List<model> listKaryawan = new ArrayList<>();

    public void tambah(String id, String nama, String jabatan){

        listKaryawan.add(new model(id, nama, jabatan));
        System.out.println("-> Karyawan berhasil ditambahkan!");
    }

    public List<model> tampilkan() {
        return listKaryawan;
    }

    public void ubah(String id, String namaBaru, String jabatanBaru) throws Exception {
        for (model k : listKaryawan) {
            if (k.getId().equalsIgnoreCase(id)) {
                if (!namaBaru.isEmpty()) k.setNama(namaBaru);
                if (!jabatanBaru.isEmpty()) k.setJabatan(jabatanBaru);
                System.out.println("-> Data berhasil diubah!");
                return;
            }
        }
        throw new Exception("Karyawan dengan ID " + id + " tidak ditemukan!");
    }

    public void hapus(String id) throws Exception {
        boolean terhapus = listKaryawan.removeIf(k -> k.getId().equalsIgnoreCase(id));
        if (!terhapus) {
            throw new Exception("Karyawan dengan ID " + id + " tidak ditemukan!");
        }
        System.out.println("-> Data berhasil dihapus!");
    }
}