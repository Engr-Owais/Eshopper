import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:sajilo_dokan/domain/model/cart.dart';
import 'package:sajilo_dokan/domain/model/product.dart';
import 'package:sajilo_dokan/domain/model/user.dart';
import 'package:sajilo_dokan/domain/repository/api_repository.dart';
import 'package:sajilo_dokan/domain/repository/local_repository.dart';
import 'package:sajilo_dokan/presentation/routes/sajilodokan_navigation.dart';

class HomeController extends GetxController {
  final ApiRepositoryInterface apiRepositoryInterface;
  final LocalRepositoryInterface localRepositoryInterface;
  HomeController(
      {required this.apiRepositoryInterface,
      required this.localRepositoryInterface});

  Rx<User> user = User.empty().obs;
  RxInt selectedIndex = 0.obs;
  var productList = <Product>[].obs;
  RxBool isLoading = true.obs;

  RxBool isFavorite = false.obs;
  var cartList = <Cart>[].obs;
  RxBool isCartLoad = false.obs;
  RxDouble totalAmount = 0.0.obs;
  var total;

  RxList selectedCarts = [].obs;

  void refreshTotal() async {
    total = 0.0;
    cartList.forEach((element) {
      if (selectedCarts.contains(element.id)) {
        total += element.amount;
      }
    });
    totalAmount(total);
  }

  bool get isAllCartSelected =>
      selectedCarts.length == cartList.length ? true : false;

  @override
  void onReady() {
    loadUser();
    super.onReady();
    fetchProduct();
    fetchCartList();
  }

  loadUser() {
    localRepositoryInterface.getUser().then((value) => user(value));
  }

  void updateIndexSelected(int index) {
    selectedIndex(index);
  }

  void logout() async {
    final token = await localRepositoryInterface.getToken();
    await apiRepositoryInterface.logout(token);
    await localRepositoryInterface.clearAllData();
  }

  void fetchProduct() async {
    final token = await localRepositoryInterface.getToken();
    isLoading(false);
    try {
      var products = await apiRepositoryInterface.fetchingProdcut(token);
      if (products != null) {
        productList(products);
      }
    } finally {
      isLoading(true);
    }
  }

  // void favoritebtn() {
  //   isFavorite.value = !isFavorite.value;
  // }

  void fetchCartList() async {
    final token = await localRepositoryInterface.getToken();
    try {
      isCartLoad(true);
      var carts = await apiRepositoryInterface.getCartList(token);
      print('Cartlist called');
      if (carts != null) {
        cartList(carts);
      }
    } finally {
      isCartLoad(false);
      refreshTotal();
    }
  }

  void addToCard(int? id) async {
    final token = await localRepositoryInterface.getToken();
    if (token != null) {
      if (!isCartLoad.value) {
        var result = await apiRepositoryInterface.addToCart(token, id);

        fetchCartList();
        if (result == true) {
          Get.snackbar('Added to cart successfully!', '',
              snackPosition: SnackPosition.BOTTOM,
              colorText: Colors.white,
              borderRadius: 0,
              backgroundColor: Colors.black.withOpacity(0.8),
              isDismissible: true,
              margin: EdgeInsets.all(0),
              padding: EdgeInsets.all(5)
              // animationDuration: Duration(seconds: 1),
              // duration: Duration(seconds: 2),
              );
        }
      }
    } else {
      Get.offNamed(SajiloDokanRoutes.login);
    }
  }

  void removeProductFromCart(int? id) async {
    final token = await localRepositoryInterface.getToken();

    await apiRepositoryInterface.deleteCart(token, id);
    fetchCartList();
  }

  void clearCart() {
    cartList.clear();
  }
}
