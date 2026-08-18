package mvcjava.model;

public class model {
    private String id;
    private String nama;
    private String jabatan;

    public model(String id, String nama, String jabatan) {
        this.id = id;
        this.nama = nama;
        this.jabatan = jabatan;
    }

    public String getId() { return id; }
    public String getNama() { return nama; }
    public String getJabatan() { return jabatan; }

    public void setNama(String nama) { this.nama = nama; }
    public void setJabatan(String jabatan) { this.jabatan = jabatan; }

    @Override
    public String toString() {
        return "ID: " + id + " | Nama: " + nama + " | Jabatan: " + jabatan;
    }
}

