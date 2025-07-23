package org.workshop.coffee.service;
import org.springframework.stereotype.Service;
import org.workshop.coffee.domain.Product;
import org.workshop.coffee.repository.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import java.util.List;



@Service
public class ProductService {

    @Autowired
    private ProductRepository productRepository;

    public Product save(Product product) {
        return productRepository.save(product);
    }

    // Method to delete a product by id
    public void delete(Long productId) {
        productRepository.deleteById(productId);
    }

    // Method to get a product by id
    public Product getProduct(Long productId) {
        return productRepository.findById(productId).get();
    }

    // Method to get all products
    public List<Product> getAllProducts() {
        return productRepository.findAll();
    }

    // Method to get a product by name
    public Product getProductByName(String name) {
        return productRepository.findProductByProductName(name);
    }

}