from database.DB_connect import DBConnect
from model.daily_sale import DailySale
from model.product import Product


class DAO():
    @staticmethod
    def getYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from go_daily_sales gds"""

        cursor.execute(query)

        for row in cursor:
            result.append(DailySale(row["Retailer_code"], row["Product_number"], row["Order_method_code"],
                                    row["Date"], row["Quantity"], row["Unit_price"], row["Unit_sale_price"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getColors():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from go_products gp"""

        cursor.execute(query)

        for row in cursor:
            result.append(Product(row["Product_number"], row["Product_line"], row["Product_type"],
                                  row["Product"], row["Product_brand"], row["Product_color"],
                                  row["Unit_cost"], row["Unit_price"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(color):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from go_products gp
                    where gp.Product_color = %s"""

        cursor.execute(query, (color, ))

        for row in cursor:
            result.append(Product(row["Product_number"], row["Product_line"], row["Product_type"],
                                  row["Product"], row["Product_brand"], row["Product_color"],
                                  row["Unit_cost"], row["Unit_price"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(p1, p2, anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select count(distinct gds.`Date`) as N
                    from go_daily_sales gds, go_daily_sales gds2 
                    where gds.Retailer_code = gds2.Retailer_code
                    and gds.`Date` = gds2.`Date` 
                    and gds.Product_number = %s
                    and gds2.Product_number = %s
                    and year(gds.`Date`) = %s"""

        cursor.execute(query, (p1._Product_number, p2._Product_number, str(anno)))

        for row in cursor:
            result.append(row["N"])

        cursor.close()
        conn.close()
        return result



