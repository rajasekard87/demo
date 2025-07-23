package org.workshop.coffee.service;
import org.workshop.coffee.domain.Order;
import org.workshop.coffee.domain.Person;
import org.workshop.coffee.repository.OrderRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;




@ExtendWith(MockitoExtension.class)
public class OrderServiceTest {

    @Mock
    private OrderRepository orderRepository;

    @InjectMocks
    private OrderService orderService;

    @Test
    public void testSaveOrder() {
        Order order = new Order();
        when(orderRepository.save(order)).thenReturn(order);

        Order savedOrder = orderService.save(order);

        assertEquals(order, savedOrder);
    }

    @Test
    public void testDeleteOrder() {
        Order order = new Order();

        orderService.delete(order);

        verify(orderRepository).delete(order);
    }

    @Test
    public void testFindByPerson() {
        Person person = new Person();
        List<Order> expectedOrders = new ArrayList<>();
        when(orderRepository.findOrderByPerson(person)).thenReturn(expectedOrders);

        List<Order> orders = orderService.findByPerson(person);

        assertEquals(expectedOrders, orders);
    }

    @Test
    public void testFindByDate() {
        Date minDate = new Date();
        Date maxDate = new Date();
        List<Order> expectedOrders = new ArrayList<>();
        when(orderRepository.findOrderByOrderDateBetween(minDate, maxDate)).thenReturn(expectedOrders);

        List<Order> orders = orderService.findByDate(minDate, maxDate);

        assertEquals(expectedOrders, orders);
    }

    @Test
    public void testFindAllOrders() {
        List<Order> expectedOrders = new ArrayList<>();
        when(orderRepository.findAll()).thenReturn(expectedOrders);

        List<Order> orders = orderService.findAll();

        assertEquals(expectedOrders, orders);
    }
}