package net.cpbackend.stanza;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.http.HttpStatus.BAD_REQUEST;
import static org.springframework.http.HttpStatus.NOT_FOUND;

import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.junit4.SpringRunner;

import net.cpbackend.model.Stanza;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class InvalidStanzaTest {

	@Autowired
	private TestRestTemplate restTemplate;
	
	@Test
	void createStanzaInvalidData() {
		ResponseEntity<Stanza> response = restTemplate.postForEntity("/officina/stanze", new Stanza(),
				Stanza.class);

		assertEquals(BAD_REQUEST.value(), response.getStatusCode().value());
	}
	

	@Test
	void findByIdNotFound() {
		ResponseEntity<Stanza> response = restTemplate.getForEntity("/officina/stanze/{id}",
				Stanza.class, Long.MAX_VALUE);

		assertEquals(NOT_FOUND.value(), response.getStatusCode().value());
	}
	
	@Test
	void updateStanzaInvalidData() {
		ResponseEntity<Stanza> response = restTemplate.exchange("/officina/stanze/{id}", HttpMethod.PUT,
				new HttpEntity<>(null), Stanza.class, 1L);

		assertEquals(BAD_REQUEST.value(), response.getStatusCode().value());
	}
	
	@Test
	void updateStanzaNotFound() {
		Stanza stanza = new Stanza();
		stanza.setId(Long.MAX_VALUE);

		ResponseEntity<Stanza> response = restTemplate.exchange("/officina/stanze/{id}", HttpMethod.PUT,
				new HttpEntity<>(stanza), Stanza.class, Long.MAX_VALUE);

		assertEquals(NOT_FOUND.value(), response.getStatusCode().value());
	}
	
	@Test
	void deleteStanzaNotFound() {
		ResponseEntity<Stanza> response = restTemplate.exchange("/officina/stanze/{id}", HttpMethod.DELETE,
				null, Stanza.class, Long.MAX_VALUE);

		assertEquals(NOT_FOUND.value(), response.getStatusCode().value());
	}
}