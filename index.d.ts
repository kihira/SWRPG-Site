declare namespace DataTables {
    interface ColumnMethods extends CoreMethods, CommonColumnMethod {
        index(): number;

        index(t: string): Api;
    }
}
