package org.workshop.coffee.repository;

import org.workshop.coffee.domain.Product;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.sql.DataSource;
import java.util.List;
import java.util.Locale;

@Repository
public class SearchRepository {

    @PersistenceContext
    private EntityManager em;

    @Autowired
    DataSource dataSource;

    public List<Product> searchProduct(String input) {
        input = input.toLowerCase(Locale.ROOT);
        String query = "SELECT p FROM Product p WHERE LOWER(p.productName) LIKE :input OR LOWER(p.description) LIKE :input";
        List<Product> products = em.createQuery(query, Product.class)
                .setParameter("input", "%" + input + "%")
                .getResultList();
        return products;
    }
}