/**
 * This class is responsible for providing user details for authentication and authorization purposes.
 * It implements the UserDetailsService interface provided by Spring Security.
 */
package org.workshop.coffee.service;

import org.workshop.coffee.repository.PersonRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CustomUserDetailsService implements UserDetailsService {

    @Autowired
    PersonRepository personRepository;

    /**
     * This method loads user details by username.
     * It retrieves the user from the person repository based on the provided username.
     * If the user is not found, it throws a UsernameNotFoundException.
     * Otherwise, it creates a SimpleGrantedAuthority object based on the user's roles,
     * and returns a User object containing the username, encrypted password, and authorities.
     *
     * @param username the username of the user
     * @return UserDetails object containing user details
     * @throws UsernameNotFoundException if the user is not found
     */
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        var user = personRepository.findByUsername(username);
        if (user == null) {
            throw new UsernameNotFoundException(username);
        }

        var role = new SimpleGrantedAuthority(user.getRoles().toString());
        return new User(user.getUsername(), user.getEncryptedPassword(), List.of(role));
    }
}