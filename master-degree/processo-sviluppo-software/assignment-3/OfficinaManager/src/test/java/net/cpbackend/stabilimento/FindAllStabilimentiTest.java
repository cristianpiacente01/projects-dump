package net.cpbackend.stabilimento;

import static org.junit.Assert.assertTrue;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.http.HttpStatus.OK;

import java.util.HashSet;
import java.util.Set;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.junit4.SpringRunner;

import net.cpbackend.model.Stabilimento;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class FindAllStabilimentiTest {
	
	@Autowired
	private TestRestTemplate restTemplate;
	
	private Set<Stabilimento> stabilimenti;
	
	@BeforeEach
	void setUp() {
		stabilimenti = new HashSet<>();
		
		for (int i = 0; i < 3; ++i) {
			Stabilimento stabilimento = new Stabilimento("test");
			stabilimento.setId(restTemplate.postForEntity("/officina/stabilimenti", stabilimento, Stabilimento.class).getBody().getId());
			
			if (stabilimento.getId() == null) throw new RuntimeException("Failed to initialize a stabilimento");
			
			stabilimenti.add(stabilimento);
		}
	}
	
	@AfterEach
	void tearDown() {
		for (Stabilimento stabilimento : stabilimenti) {
			restTemplate.exchange("/officina/stabilimenti/{id}", HttpMethod.DELETE,
					null, Stabilimento.class, stabilimento.getId());
		}
	}
	
	@Test
	void findAll() {
		ResponseEntity<Set<Stabilimento>> response = restTemplate.exchange("/officina/stabilimenti", HttpMethod.GET,
				null, new ParameterizedTypeReference<Set<Stabilimento>>() {
				});

		assertEquals(OK.value(), response.getStatusCode().value());
		
		assertTrue(response.getBody().containsAll(stabilimenti));
	}
}