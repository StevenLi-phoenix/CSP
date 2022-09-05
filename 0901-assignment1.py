import pprint
import threading
import uuid
import flask
from flask import Response, Request, request, make_response, jsonify
from werkzeug.serving import make_server
import atexit

print = pprint.pprint


class item:
    def __init__(self, number_bids=0, reserve_price=0, description="None description"):
        self._uuid = uuid.uuid4()
        self._number_bids = number_bids
        self.reserve_price = reserve_price
        self.description = description
        self.highest_price = 0
        self.STATUS = False
        self._lock = {
            "lock": False,
            "thread": threading.current_thread(),
        }
        self.LastBuyerId = None

    def describe(self, noOutput=False):
        a = {
            "Uuid": self._uuid,
            "Number of bids": self._number_bids,
            "Reserve price": self.reserve_price,
            "Description": self.description,
            "Highest Price": self.highest_price,
            "Last buyer": self.LastBuyerId,
        }
        if noOutput:
            return a
        else:
            print(a)

    def buy(self, price, buyer_id):
        self.STATUS = True
        if self._lock["lock"]:
            print("Current session is locked by other threads.")
            return False
        self._lock["_lock"] = True
        self._lock["thread"] = threading.current_thread()
        if price > self.highest_price:
            self.highest_price = price
            self._number_bids += 1
            self.LastBuyerId = buyer_id
            self._lock["_lock"] = False
            return True
        else:
            print("Price is lower than highest price")
            self._lock["_lock"] = False
            return False

    @property
    def uuid(self):
        return self._uuid


class buyer:
    def __init__(self):
        self._uuid = uuid.uuid4()
        self._number_bids = 0

    def buy(self, item, price, buyer_id=None):
        if buyer_id is None:
            buyer_id = self._uuid
        self._number_bids += 1
        return item.buy(price, buyer_id=buyer_id)

    def describe(self):
        print(
            {
                "Uuid": self._uuid,
            }
        )

    def buyer_thread(self):  # use a thread to start this
        global items
        self.describe()
        option = ""
        while option != "q":
            option = str(input(f"Options[q(Quit), b[1-{len(items)}](Buy), q[1-{len(items)}](Query), qa(Query All)]:"))
            if option.startswith("b"):
                if len(option) > 1:
                    try:
                        item_index = int(option[1:]) - 1
                    except ValueError as e:
                        print(f"Unknown parameter at {option}:{e}")
                        continue
                else:
                    item_index = int(input("Input item index:")) - 1
                price = float(input("Input price:"))
                try:
                    assert 0 <= item_index < len(items) and type(item_index) is int, "item index out of item index"
                    assert 0 <= price, "Please input positive number of price"
                except AssertionError as e:
                    print("Failed")
                    print(e)
                    continue
                if self.buy(items[item_index], price):
                    print("Success")
                    items[item_index].describe()
                else:
                    print("Failed")
            elif option.startswith("q") and option != "q":
                if option[1:] == "a":
                    for i in items:
                        i.describe()
                else:
                    try:
                        items[int(option[1:])].describe()
                    except:
                        pass
            else:
                print(f"Option {option} not in options [q, q[1-], b, b[1-], qa]")


def describe_items(items):
    for it in items:
        it.describe()


def describe_buyers(buyers):
    for bu in buyers:
        bu.describe()


class ServerThread(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()


app = flask.Flask("auction")


@app.route("/start")
def start_server():
    global server
    server = ServerThread(app)
    server.start()


@app.route("/stop")
def stop_server():
    global server
    server.shutdown()
atexit.register(lambda:stop_server)



@app.route("/queryInfo&subject=info")
def sequeryInfo():
    a = ""
    if a == "ALL":
        info = {
            "items": describe_items(items),
            "buyers": describe_buyers(buyers),
        }
    elif a == "items":
        info = {
            "items": describe_items(items),
        }
        return jsonify(info)
    elif a == "buyers":
        info = {
            "buyers": describe_buyers(items),
        }
    else:
        info = {}
    return jsonify(info)


@app.route("/item&subject=index")
def sequeryItem():
    a = 1
    try:
        int(a)
    except ValueError:
        return {}
    return jsonify(items[int(a)].describe())


@app.route("/buyer&subject=index")
def se_queryItem():  # 好名字都被狗取了
    a = 1
    try:
        int(a)
    except ValueError:
        return {}
    return jsonify(buyers[int(a)].describe())


@app.route("/test")
def test():
    return


@app.after_request
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


global items, server
if __name__ == "__main__":
    start_server()
    items = [item(reserve_price=i, description=f"商品{i}（{i}）") for i in range(10)]
    buyers = [buyer() for i in range(10)]
    ts = []
    print("Items:")
    describe_items(items)
    print("Buyers:")
    describe_buyers(buyers)
    buyer_index = int(input(f"Input buyer number(1-{len(buyers)}):"))
    buyer = buyers[buyer_index - 1]
    t = threading.Thread(target=buyer.buyer_thread)
    t.start()
    ts.append(t)
    for t in ts:
        t.join()
    total_price = 0
    abortive_auction = []
    none_price = []
    sold = []
    for i in items:
        if i.STATUS:
            if i.reserve_price < i.highest_price:
                total_price += i.highest_price * 1.1
                sold.append(i.uuid)
            else:
                abortive_auction.append(i.uuid)
        else:
            none_price.append(i.uuid)
    info = {
        "Total price": round(total_price, 2),
        "Sold": sold,
        "Abortice auction": abortive_auction,
        "None price auction": none_price,
        "the number of items sold": {len(sold)},
        "the number of items that did not meet the reserve price": {len(abortive_auction)},
        "the number of items with no bids": {len(none_price)},
    }
    print(info)
    stop_server()
    # describe_items(items)
