
import streamlit as st
from userdata import (
    get_user_data,
    get_order_data,
    get_orderitem_data,
    get_orderitem_detail,
    update_order_status
)
import pandas as pd

headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()


def user_data_table():
    df = pd.DataFrame(get_user_data())
    return df


def show_main_page():
    with mainSection:
        st.header('Admin Panel')

        user, orders = st.tabs(['Users', 'Orders'])

        with user:
            st.subheader('User Data Display')
            s = user_data_table()
            st.table(s)

        with orders:
            st.subheader('Order Data Display')

            order_df = pd.DataFrame(get_order_data())
            st.dataframe(order_df, use_container_width=True)

            st.subheader('Select the Order ID')

            order_id = st.number_input(
                label="Enter Order ID",
                min_value=1,
                step=1
            )

            if st.button("Get Order Details"):
                orderitem_pd = pd.DataFrame(
                    get_orderitem_detail(order_id)
                )
                st.table(orderitem_pd)

            st.subheader("Update Order Status")

            selected_status = st.selectbox(
                "Select Order Status",
                [
                    "Pending",
                    "Confirmed",
                    "Preparing",
                    "Out for Delivery",
                    "Delivered"
                ]
            )

            if st.button("Update Status"):
                result = update_order_status(
                    order_id,
                    selected_status
                )

                if result is not False:
                    st.success("Order status updated successfully!")
                    st.rerun()
                else:
                    st.error("Unable to update order status.")


def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False


def show_logout_page():
    loginSection.empty()
    with logOutSection:
        st.button(
            "Log Out",
            key="logout",
            on_click=LoggedOut_Clicked
        )


def LoggedIn_Clicked(email_id, password):
    if email_id == 'admin' and password == 'admin':
        st.session_state['loggedIn'] = True
    else:
        st.session_state['loggedIn'] = False
        st.error("Invalid user name or password")


def show_login_page():
    with loginSection:
        if st.session_state['loggedIn'] == False:
            st.subheader('Login Here 🎉')

            email_id = st.text_input(
                label="",
                value="",
                placeholder="Enter your user name"
            )

            password = st.text_input(
                label="",
                value="",
                placeholder="Enter password",
                type="password"
            )

            st.button(
                "Login",
                on_click=LoggedIn_Clicked,
                args=(email_id, password)
            )


with headerSection:
    st.title("Online Food Ordering System - Admin Login")

    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False

    if st.session_state['loggedIn']:
        show_logout_page()
        show_main_page()
    else:
        show_login_page()
