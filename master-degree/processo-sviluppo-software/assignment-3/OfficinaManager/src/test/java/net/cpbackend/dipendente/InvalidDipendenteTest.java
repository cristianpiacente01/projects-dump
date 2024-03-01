package net.cpbackend.dipendente;

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

import net.cpbackend.model.Dipendente;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class InvalidDipendenteTest {

	@Autowired
	private TestRestTemplate restTemplate;
	
	@Test
	void createDipendenteInvalidData() {
		ResponseEntity<Dipendente> response = restTemplate.postForEntity("/officina/dipendenti", new Dipendente(),
				Dipendente.class);

		assertEquals(BAD_REQUEST.value(), response.getStatusCode().value());
	}
	

	@Test
	void findByIdNotFound() {
		ResponseEntity<Dipendente> response = restTemplate.getForEntity("/officina/dipendenti/{id}",
				Dipendente.class, Long.MAX_VALUE);

		assertEquals(NOT_FOUND.value(), response.getStatusCode().value());
	}
	
	@Test
	void updateDipendenteInvalidData() {
		ResponseEntity<Dipendente> response = restTemplate.exchange("/officina/dipendenti/{id}", HttpMethod.PUT,
				new HttpEntity<>(null), Dipendente.class, 1L);

		assertEquals(BAD_REQUEST.value(), response.getStatusCode().value());
	}
	
	@Test
	void updateDipendenteNotFound() {
		Dipendente dipendente = new Dipendente();
		dipendente.setId(Long.MAX_VALUE);

		ResponseEntity<Dipendente> response = restTemplate.exchange("/officina/dipendenti/{id}", HttpMethod.PUT,
				new HttpEntity<>(dipendente), Dipendente.class, Long.MAX_VALUE);

		assertEquals(NOT_FOUND.value(), response.getStatusCode().value());
	}
	
	@Test
	void deleteDipendenteNotFound() {
		ResponseEntity<Dipendente> response = restTemplate.exchange("/officina/dipendenti/{id}", HttpMethod.DELETE,
				null, Dipendente.class, Long.MAX_VALUE);

		assertEquals(NOT_FOUND.value(), response.getStatusCode().value());
	}
}