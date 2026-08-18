import oop2.controller.controller;
import oop2.view.view;

public class main {
    public static void main(String[] args) {
        controller appController = new controller();
        view appView = new view(appController);

        appView.showMenu();
    }
}