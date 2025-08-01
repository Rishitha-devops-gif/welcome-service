package com.transfleet.welcome_service;
 
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
 
@RestController
public class WelcomeController {
 
    @GetMapping("/")
    public String welcome() {
        return "Welcome to TransFleet's Cloud Microservice!";
    }
}
