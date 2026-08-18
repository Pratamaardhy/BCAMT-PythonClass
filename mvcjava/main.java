package mvcjava;
import mvcjava.controller.controller;
import mvcjava.view.view;

public class main {
    public static void main(String[] args) {
        controller appController = new controller();
        view appView = new view(appController);

        appView.showMenu();
    }
}
