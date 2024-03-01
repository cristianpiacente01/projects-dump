package net.cpbackend.attrezzo;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.http.HttpStatus.BAD_REQUEST;
import static org.springframework.http.HttpStatus.NOT_FOUND;

import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.test.context.junit4.SpringRunner;

import net.cpbackend.model.Motosega;
import net.cpbackend.model.Trapano;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class InvalidAttrezzoTest {
	
	// test invalid data for both motosega and trapano

	@Autowired
	private TestRestTemplate restTemplate;
	
	@Test
	void createAttrezzoInvalidData() {
		assertEquals(BAD_REQUEST.value(), restTemplate.postForEntity("/officina/attrezzi", new Motosega(),
				Motosega.class).getStatusCode().value());

		assertEquals(BAD_REQUEST.value(), restTemplate.postForEntity("/officina/attrezzi", new Trapano(),
				Trapano.class).getStatusCode().value());
	}
	
	@Test
	void findByIdNotFound() {
		// let's suppose Long.MAX_VALUE is not a valid id on the db
		
		assertEquals(NOT_FOUND.value(), restTemplate.getForEntity("/officina/attrezzi/{id}",
				Motosega.class, Long.MAX_VALUE).getStatusCode().value());

		assertEquals(NOT_FOUND.value(), restTemplate.getForEntity("/officina/attrezzi/{id}",
				Trapano.class, Long.MAX_VALUE).getStatusCode().value());
	}
	
	@Test
	void updateAttrezzoInvalidData() {
		// the request body doesn't get passed so it's a bad request
		
		assertEquals(BAD_REQUEST.value(), restTemplate.exchange("/officina/attrezzi/{id}", HttpMethod.PUT,
				new HttpEntity<>(null), Motosega.class, 1L).getStatusCode().value());

		assertEquals(BAD_REQUEST.value(), restTemplate.exchange("/officina/attrezzi/{id}", HttpMethod.PUT,
				new HttpEntity<>(null), Trapano.class, 1L).getStatusCode().value());
	}
	
	@Test
	void updateAttrezzoNotFound() {
		// the id gets matched but the attrezzo is not on the db so it doesn't get found
		
		Motosega motosega = new Motosega();
		motosega.setId(Long.MAX_VALUE);

		assertEquals(NOT_FOUND.value(), restTemplate.exchange("/officina/attrezzi/{id}", HttpMethod.PUT,
				new HttpEntity<>(motosega), Motosega.class, Long.MAX_VALUE).getStatusCode().value());
		
		Trapano trapano = new Trapano();
		trapano.setId(Long.MAX_VALUE);

		assertEquals(NOT_FOUND.value(), restTemplate.exchange("/officina/attrezzi/{id}", HttpMethod.PUT,
				new HttpEntity<>(trapano), Trapano.class, Long.MAX_VALUE).getStatusCode().value());
	}
	
	@Test
	void deleteAttrezzoNotFound() {
		// let's suppose Long.MAX_VALUE is not a valid id on the db
		
		assertEquals(NOT_FOUND.value(), restTemplate.exchange("/officina/attrezzi/{id}", HttpMethod.DELETE,
				null, Motosega.class, Long.MAX_VALUE).getStatusCode().value());
		
		assertEquals(NOT_FOUND.value(), restTemplate.exchange("/officina/attrezzi/{id}", HttpMethod.DELETE,
				null, Trapano.class, Long.MAX_VALUE).getStatusCode().value());
	}
	
	@Test
	void searchAttrezzoInvalidData() {
		// X is not a valid attrezzo type
		
		assertEquals(BAD_REQUEST.value(), restTemplate.exchange("/officina/attrezzi/search/{tipo}/{potenza}/{piano}", 
				HttpMethod.GET,
				null, new ParameterizedTypeReference<>() {},
				'X', 0, 0).getStatusCode().value());
	}
}