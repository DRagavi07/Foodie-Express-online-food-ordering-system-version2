
import streamlit as st
import pandas as pd
import time

from userdata import (
    login, signup, get_details, place_order,
    update_details, update_password, delete_user,
    get_user_order_history
)

st.set_page_config(
    page_title="Foodie Express",
    page_icon="🍔",
    layout="wide"
)

# ---------------- PAGE NAMES ----------------

page_names = [
    "🍔 Food Menu",
    "🛒 Shopping Cart",
    "🚚 Order Tracking",
    "📜 Order History",
    "👤 My Account"
]

# ---------------- SESSION STATE ----------------

if "loggedIn" not in st.session_state:
    st.session_state["loggedIn"] = False

if "checkout" not in st.session_state:
    st.session_state["checkout"] = False

if "details" not in st.session_state:
    st.session_state["details"] = None

if "food_list" not in st.session_state:
    st.session_state["food_list"] = [None] * 9

if "qty_list" not in st.session_state:
    st.session_state["qty_list"] = [None] * 9

if "amt_list" not in st.session_state:
    st.session_state["amt_list"] = [None] * 9

if "current_page" not in st.session_state:
    st.session_state["current_page"] = 0

if "top_navigation" not in st.session_state:
    st.session_state["top_navigation"] = page_names[0]


# ---------------- PAGE NAVIGATION ----------------

def sync_navigation():

    st.session_state["current_page"] = page_names.index(
        st.session_state["top_navigation"]
    )


def next_page():

    if st.session_state["current_page"] < 4:
        st.session_state["current_page"] += 1

    st.session_state["top_navigation"] = page_names[
        st.session_state["current_page"]
    ]


def previous_page():

    if st.session_state["current_page"] > 0:
        st.session_state["current_page"] -= 1

    st.session_state["top_navigation"] = page_names[
        st.session_state["current_page"]
    ]


# ---------------- CART RESET ----------------

def clear_cart():

    st.session_state["food_list"] = [None] * 9
    st.session_state["qty_list"] = [None] * 9
    st.session_state["amt_list"] = [None] * 9

    for i in range(9):
        st.session_state.pop(f"food_{i}", None)
        st.session_state.pop(f"qty_{i}", None)

    st.session_state["current_page"] = 0
    st.session_state["top_navigation"] = page_names[0]


# ---------------- LOGOUT ----------------

def LoggedOut_Clicked():

    st.session_state["loggedIn"] = False
    st.session_state["details"] = None
    st.session_state["checkout"] = False

    clear_cart()


# ---------------- ORDER PLACEMENT ----------------

def order_pressed(user_id, total_amt, paymentmethod, food_list, qty_list):

    if place_order(
        user_id,
        total_amt,
        paymentmethod,
        food_list,
        qty_list
    ):

        clear_cart()

        st.session_state["checkout"] = True
        st.session_state["loggedIn"] = False

    else:

        st.error("Order could not be placed. Please try again.")


# ---------------- CHECKOUT PAGE ----------------

def show_checkout_page():

    st.title("🎉 Order Successful!")

    my_bar = st.progress(0)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1)

    st.success(
        f"Hey {st.session_state['details'][1]}, "
        "Your Order has been placed Successfully!"
    )

    st.balloons()

    st.subheader(
        f"Delivery Address: {st.session_state['details'][2]}"
    )

    st.subheader(
        f"Contact Number: {st.session_state['details'][3]}"
    )

    st.info("Thank you for ordering with Foodie Express! ❤️")

    if st.button("Continue Shopping", use_container_width=True):

        st.session_state["checkout"] = False
        st.session_state["loggedIn"] = True
        st.session_state["current_page"] = 0
        st.session_state["top_navigation"] = page_names[0]

        st.rerun()


# ---------------- ACCOUNT UPDATE ----------------

def update_user_details(user_id, email, name, address, number):

    if update_details(user_id, email, name, address, number):

        st.session_state["details"] = get_details(email)

        st.success("User Information Updated Successfully!")

        st.rerun()

    else:

        st.error("Error while updating information")


def update_user_password(user_id, password):

    if update_password(user_id, password):

        st.success("Password updated successfully!")

    else:

        st.error("Error while updating password")


# ---------------- DELETE ACCOUNT ----------------

def delete_user_show(user_id):

    delete_user(user_id)

    LoggedOut_Clicked()

    st.success("Account Deleted Successfully")

    st.rerun()


# ---------------- MAIN CUSTOMER PAGE ----------------

def show_main_page():

    food_list = st.session_state["food_list"]
    qty_list = st.session_state["qty_list"]
    amt_list = st.session_state["amt_list"]

    # ---------------- TOP NAVIGATION ----------------

    st.header(
        f"Welcome {st.session_state['details'][1]} 😎"
    )

    st.radio(
        "Select Page",
        page_names,
        horizontal=True,
        key="top_navigation",
        on_change=sync_navigation,
        label_visibility="collapsed"
    )

    page = st.session_state["current_page"]

    st.caption(f"Page {page + 1} of 5")

    st.divider()

    # ---------------- PAGE 1 - FOOD MENU ----------------

    if page == 0:

        st.title("🍴 Our Delicious Food Menu")

        st.write("Choose your favourite food and enjoy!")

        food_items = [
            ("Pizza", "🍕", "Delicious cheesy pizza with fresh toppings.", 199, "pizza.jpg"),
            ("Burger", "🍔", "Tasty burger with fresh vegetables.", 99, "burger.jpg"),
            ("Noodles", "🍜", "Hot and delicious noodles.", 149, "noodles.jpg"),
            ("Chicken Biryani", "🍗", "Spicy and flavourful chicken biryani.", 180, "chicken_biryani.jpg"),
            ("Veg Fried Rice", "🍚", "Delicious fried rice with fresh vegetables.", 120, "veg_fried_rice.jpg"),
            ("Chicken Noodles", "🍝", "Tasty chicken noodles with spices.", 160, "chicken_noodles.jpg"),
            ("Paneer Pizza", "🧀", "Cheesy pizza topped with fresh paneer.", 220, "paneer_pizza.jpg"),
            ("French Fries", "🍟", "Crispy and golden french fries.", 90, "french_fries.jpg"),
            ("Chicken Burger", "🍔", "Juicy chicken burger with fresh toppings.", 149, "chicken_burger.jpg")
        ]

        for row_start in range(0, len(food_items), 3):

            cols = st.columns(3)

            for col_index, index in enumerate(
                range(row_start, min(row_start + 3, len(food_items)))
            ):

                name, emoji, description, price, image = food_items[index]

                with cols[col_index]:

                    st.image(image, width=250)

                    st.subheader(f"{emoji} {name}")

                    st.write(description)

                    st.markdown(f"### ₹{price}")

                    selected = st.checkbox(
                        f"Order {name}",
                        key=f"food_{index}"
                    )

                    if selected:

                        quantity = st.number_input(
                            "Select Quantity",
                            min_value=1,
                            value=1,
                            step=1,
                            key=f"qty_{index}"
                        )

                        food_list[index] = name.lower()
                        qty_list[index] = int(quantity)
                        amt_list[index] = int(quantity) * price

                    else:

                        food_list[index] = None
                        qty_list[index] = None
                        amt_list[index] = None

        selected_count = sum(
            1 for food in food_list if food is not None
        )

        st.info(f"Selected food items: {selected_count}")

    # ---------------- PAGE 2 - SHOPPING CART ----------------

    elif page == 1:

        st.title("🛒 Your Shopping Cart")

        order = {
            "Food Name": food_list,
            "Quantity": qty_list,
            "Amount (₹)": amt_list
        }

        cart_df = pd.DataFrame(order).dropna()

        if cart_df.empty:

            st.info(
                "Your cart is empty. Please select some food in Food Menu!"
            )

        else:

            st.dataframe(
                cart_df,
                use_container_width=True,
                hide_index=True
            )

            total_amt = sum(
                amt for amt in amt_list if amt is not None
            )

            total_item = [
                food for food in food_list if food is not None
            ]

            total_qty = [
                qty for qty in qty_list if qty is not None
            ]

            st.subheader(f"Your Total Amount: ₹{total_amt}")

            st.warning(
                "Demo Payment Only - No real money will be charged."
            )

            payment = st.selectbox(
                "Choose Demo Payment Method",
                [
                    "Cash",
                    "UPI",
                    "Net Banking",
                    "Credit Card",
                    "Debit Card"
                ]
            )

            st.button(
                "Place Your Order",
                on_click=order_pressed,
                args=(
                    st.session_state["details"][0],
                    total_amt,
                    payment,
                    total_item,
                    total_qty
                ),
                use_container_width=True
            )

    # ---------------- PAGE 3 - ORDER TRACKING ----------------

    elif page == 2:

        st.title("🚚 Track Your Order")

        user_id = st.session_state["details"][0]

        tracking_df = pd.DataFrame(
            get_user_order_history(user_id)
        )

        if tracking_df.empty:

            st.info("You have no orders to track.")

        else:

            order_ids = tracking_df["Order ID"].unique().tolist()

            selected_order = st.selectbox(
                "Select Your Order ID",
                order_ids,
                key="tracking_order_id"
            )

            selected_order_df = tracking_df[
                tracking_df["Order ID"] == selected_order
            ]

            st.subheader(f"Order #{selected_order}")

            st.table(selected_order_df)

            current_status = selected_order_df.iloc[0]["Order Status"]

            status_steps = [
                "Pending",
                "Confirmed",
                "Preparing",
                "Out for Delivery",
                "Delivered"
            ]

            st.subheader("📦 Order Progress")

            if current_status in status_steps:

                current_index = status_steps.index(current_status)

                progress_value = (
                    current_index + 1
                ) / len(status_steps)

                st.progress(progress_value)

                for index, status in enumerate(status_steps):

                    if index < current_index:

                        st.success(f"✓ {status}")

                    elif index == current_index:

                        st.info(f"📍 Current Status: {status}")

                    else:

                        st.write(f"○ {status}")

            else:

                st.warning(f"Current Status: {current_status}")

    # ---------------- PAGE 4 - ORDER HISTORY ----------------

    elif page == 3:

        st.title("📜 My Order History")

        user_id = st.session_state["details"][0]

        history_df = pd.DataFrame(
            get_user_order_history(user_id)
        )

        if history_df.empty:

            st.info("You have no previous orders.")

        else:

            st.write("Here are all your previous orders:")

            st.dataframe(
                history_df,
                use_container_width=True,
                hide_index=True
            )

    # ---------------- PAGE 5 - MY ACCOUNT ----------------

    elif page == 4:

        st.title("👤 My Account")

        st.subheader("Update Your Details")

        up_email = st.text_input(
            "Email",
            value=str(st.session_state["details"][4]),
            key="account_email"
        )

        up_name = st.text_input(
            "Name",
            value=str(st.session_state["details"][1]),
            key="account_name"
        )

        up_address = st.text_input(
            "Address",
            value=str(st.session_state["details"][2]),
            key="account_address"
        )

        up_number = st.text_input(
            "Phone Number",
            value=str(st.session_state["details"][3]),
            key="account_phone"
        )

        st.button(
            "Update User Details",
            on_click=update_user_details,
            args=(
                st.session_state["details"][0],
                up_email,
                up_name,
                up_address,
                up_number
            )
        )

        st.divider()

        if st.checkbox("Do you want to change your password?"):

            st.subheader("Update Password")

            up_passw = st.text_input(
                "New Password",
                type="password",
                key="new_password"
            )

            up_conf_passw = st.text_input(
                "Confirm New Password",
                type="password",
                key="confirm_password"
            )

            if up_passw and up_passw == up_conf_passw:

                st.button(
                    "Update Password",
                    on_click=update_user_password,
                    args=(
                        st.session_state["details"][0],
                        up_passw
                    )
                )

            elif up_conf_passw:

                st.warning("Password does not match!")

        st.divider()

        if st.checkbox("Do you want to delete your account?"):

            st.warning(
                "Are you sure you want to delete your account?"
            )

            st.button(
                "DELETE MY ACCOUNT",
                on_click=delete_user_show,
                args=(st.session_state["details"][0],)
            )

    # ---------------- PREVIOUS AND NEXT BUTTONS ----------------

    st.divider()

    previous_col, next_col = st.columns(2)

    with previous_col:

        st.button(
            "⬅️ Previous",
            on_click=previous_page,
            disabled=(page == 0),
            use_container_width=True,
            key=f"previous_{page}"
        )

    with next_col:

        st.button(
            "Next ➡️",
            on_click=next_page,
            disabled=(page == 4),
            use_container_width=True,
            key=f"next_{page}"
        )


# ---------------- LOGIN ----------------

def LoggedIn_Clicked(email_id, password):

    if login(email_id, password):

        st.session_state["loggedIn"] = True

        st.session_state["details"] = get_details(email_id)

        st.session_state["current_page"] = 0
        st.session_state["top_navigation"] = page_names[0]

    else:

        st.session_state["loggedIn"] = False
        st.session_state["details"] = None

        st.error("Invalid Email or Password")


# ---------------- SIGNUP ----------------

def signup_clicked(email, name, address, phnumber, sign_password):

    try:

        if signup(email, name, address, phnumber, sign_password):

            st.success("Signup Successful!")

            st.balloons()

        else:

            st.warning("Signup failed. Please check your details.")

    except Exception:

        st.warning(
            "Email already exists or invalid details!"
        )


# ---------------- LOGIN AND SIGNUP PAGE ----------------

def show_login_page():

    st.title("🍔 Welcome to Foodie Express")

    login_tab, signup_tab = st.tabs(
        ["Login ✨", "Signup ❤️"]
    )

    with login_tab:

        st.subheader("Welcome Back! 🎉")

        email_id = st.text_input(
            "Email Address",
            placeholder="Enter your Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            placeholder="Enter Password",
            type="password",
            key="login_password"
        )

        st.button(
            "Login",
            on_click=LoggedIn_Clicked,
            args=(email_id, password),
            use_container_width=True
        )

    with signup_tab:

        st.subheader("Create Your Account 🫶")

        email = st.text_input(
            "Email ID",
            placeholder="Enter your Email-ID",
            key="signup_email"
        )

        name = st.text_input(
            "Name",
            placeholder="Enter your Name",
            key="signup_name"
        )

        address = st.text_input(
            "Address",
            placeholder="Enter your Address",
            key="signup_address"
        )

        phnumber = st.text_input(
            "Phone Number",
            placeholder="Enter your Phone Number",
            key="signup_phone"
        )

        sign_password = st.text_input(
            "Password",
            placeholder="Enter Password",
            type="password",
            key="signup_password"
        )

        cnf_password = st.text_input(
            "Confirm Password",
            placeholder="Confirm your Password",
            type="password",
            key="signup_confirm"
        )

        if sign_password and sign_password == cnf_password:

            st.button(
                "Sign Up",
                on_click=signup_clicked,
                args=(
                    email,
                    name,
                    address,
                    phnumber,
                    sign_password
                ),
                use_container_width=True
            )

        elif cnf_password:

            st.warning("Password does not match!")


# ---------------- MAIN APPLICATION ----------------

st.title("🍔 Foodie Express 😋")

if st.session_state["loggedIn"]:

    st.button(
        "Log Out",
        on_click=LoggedOut_Clicked,
        key="logout_button"
    )

    show_main_page()

elif st.session_state["checkout"]:

    st.button(
        "Log Out",
        on_click=LoggedOut_Clicked,
        key="checkout_logout"
    )

    show_checkout_page()

else:

    show_login_page()


# ---------------- HIDE STREAMLIT MENU ----------------

hide_st_style = """
<style>
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}
</style>
"""

st.markdown(
    hide_st_style,
    unsafe_allow_html=True
)
